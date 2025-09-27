# etl_netflix.py
import pandas as pd
import numpy as np
import sqlite3   # troque por psycopg2 / sqlalchemy para Postgres
import re
from datetime import datetime

# CONFIGURAÇÃO
CSV_PATH = "netflix_titles.csv"   # caminho do CSV baixado do Kaggle
SQLITE_DB = "netflix.db"          # ou string de conexão para Postgres via SQLAlchemy

# 1. Leitura
df = pd.read_csv(CSV_PATH)

# 2. Padronização de colunas para snake_case
def to_snake(s):
    return re.sub(r'\W+', '_', s).strip('_').lower()

df.columns = [to_snake(c) for c in df.columns]

# 3. Normalizar textos em colunas categóricas
cat_cols = ['type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']
for c in cat_cols:
    if c in df.columns:
        df[c] = df[c].astype('string')

# 4. Converter date_added para DATE (algumas linhas nulas)
def parse_date(s):
    try:
        return pd.to_datetime(s, dayfirst=False).date()
    except:
        return pd.NaT

if 'date_added' in df.columns:
    df['date_added'] = df['date_added'].apply(lambda x: parse_date(x) if pd.notna(x) else pd.NaT)

# 5. Separar duration em duration_value e duration_unit
def split_duration(d):
    if pd.isna(d): return (np.nan, np.nan)
    m = re.match(r'^\s*(\d+)\s*([A-Za-z]+)', str(d))
    if m:
        return (int(m.group(1)), m.group(2).lower())
    # fallback: se contiver min ou season
    if 'min' in d.lower():
        digits = re.findall(r'\d+', d)
        return (int(digits[0]) if digits else np.nan, 'min')
    if 'season' in d.lower():
        digits = re.findall(r'\d+', d)
        return (int(digits[0]) if digits else np.nan, 'season')
    return (np.nan, np.nan)

df[['duration_value','duration_unit']] = df['duration'].apply(lambda x: pd.Series(split_duration(x)))

# 6. Preencher country nulo com "unknown"
if 'country' in df.columns:
    df['country'] = df['country'].replace({pd.NA: None})
    df['country'] = df['country'].fillna("Unknown")
    df['country'] = df['country'].str.lower().str.strip()

# 7. Normalizar rating nulo para "not_rated"
if 'rating' in df.columns:
    df['rating'] = df['rating'].fillna("not_rated").str.lower().str.strip()

# 8. padronizar listed_in (gêneros) e title
if 'listed_in' in df.columns:
    df['listed_in'] = df['listed_in'].fillna("").str.lower().str.strip()
if 'title' in df.columns:
    df['title'] = df['title'].str.strip()

# 9. Criar tabela titles_clean com colunas relevantes e tipos
titles_clean = df[[
    'show_id','type','title','director','cast','country','date_added',
    'release_year','rating','duration_value','duration_unit','listed_in','description'
]].copy()

# Ajustes de tipos
titles_clean['release_year'] = pd.to_numeric(titles_clean['release_year'], errors='coerce').astype('Int64')

# 10. Normalizar multivalor: countries (separar por ',')
def explode_multival(df, col, sep=','):
    s = df[['show_id', col]].dropna()
    rows = []
    for _, r in s.iterrows():
        vals = [v.strip() for v in str(r[col]).split(sep) if v.strip()]
        for v in vals:
            rows.append({'show_id': r['show_id'], col[:-1] if col.endswith('s') else col: v.lower()})
    return pd.DataFrame(rows)

# countries
if 'country' in titles_clean.columns:
    # alguns registros têm vários países separados por ','
    titles_by_country = explode_multival(titles_clean.rename(columns={'country':'countries'}), 'countries', sep=',')
else:
    titles_by_country = pd.DataFrame(columns=['show_id','country'])

# genres
titles_by_genre = explode_multival(titles_clean.rename(columns={'listed_in':'genres'}), 'genres', sep=',')

# 11. Análise de elenco: criar tabela cast (explode)
def explode_cast(df):
    rows = []
    for _, r in df[['show_id','cast']].dropna().iterrows():
        members = [m.strip().lower() for m in str(r['cast']).split(',') if m.strip()]
        for m in members:
            rows.append({'show_id': r['show_id'], 'actor': m})
    return pd.DataFrame(rows)

cast_df = explode_cast(titles_clean)

# 12. Salvar em SQLite (ou Postgres)
conn = sqlite3.connect(SQLITE_DB)
titles_clean.to_sql('titles_clean', conn, if_exists='replace', index=False)
titles_by_country.to_sql('titles_by_country', conn, if_exists='replace', index=False)
titles_by_genre.to_sql('titles_by_genre', conn, if_exists='replace', index=False)
cast_df.to_sql('cast', conn, if_exists='replace', index=False)
conn.close()

print("ETL finalizado. Tabelas salvas em", SQLITE_DB)
