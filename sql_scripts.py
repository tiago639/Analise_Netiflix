# analysis_netflix_corrigido.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates

# Configuração de estilo
plt.style.use('default')
sns.set_palette("husl")

def create_visualizations():
    # Conectar ao banco
    conn = sqlite3.connect("netflix.db")
    
    # 1. TOP PAÍSES COM MAIS TÍTULOS
    query_paises = """
    SELECT countrie, COUNT(*) as quantidade
    FROM titles_by_country
    WHERE countrie != 'unknown'
    GROUP BY countrie
    ORDER BY quantidade DESC
    LIMIT 15;
    """
    df_paises = pd.read_sql(query_paises, conn)
    
    plt.figure(figsize=(12, 8))
    plt.barh(df_paises['countrie'], df_paises['quantidade'])
    plt.xlabel('Número de Títulos', fontsize=12)
    plt.title('Top 15 Países com Mais Títulos na Netflix', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('top_paises.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. EVOLUÇÃO POR MÊS-ANO DE LANÇAMENTOS (CORRIGIDO)
    query_evolucao = """
    SELECT 
        strftime('%Y-%m', date_added) as mes_ano,
        COUNT(*) as quantidade
    FROM titles_clean 
    WHERE date_added IS NOT NULL
    GROUP BY mes_ano;
    """
    df_evolucao = pd.read_sql(query_evolucao, conn)
    
    # Converter mes_ano para datetime e ordenar
    df_evolucao['mes_ano_dt'] = pd.to_datetime(df_evolucao['mes_ano'], format='%Y-%m')
    df_evolucao = df_evolucao.sort_values('mes_ano_dt', ascending=True)

    plt.figure(figsize=(16, 8))
    
    # Gráfico de área - USANDO A COLUNA ORDENADA
    plt.fill_between(df_evolucao['mes_ano_dt'], df_evolucao['quantidade'], 
                     alpha=0.3, color='skyblue')
    plt.plot(df_evolucao['mes_ano_dt'], df_evolucao['quantidade'], 
             marker='o', linewidth=2, color='steelblue', markersize=4)
    
    plt.xlabel('Mês-Ano', fontsize=12, fontweight='bold')
    plt.ylabel('Número de Títulos Adicionados', fontsize=12, fontweight='bold')
    plt.title('Evolução Mensal de Adições na Netflix', fontsize=14, fontweight='bold')
    
    # Formatar eixo X CORRETAMENTE
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # a cada 6 meses
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # Definir os ticks manualmente para garantir ordenação correta
    plt.xticks(df_evolucao['mes_ano_dt'][::6], rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajustar limites do eixo Y
    max_val = df_evolucao['quantidade'].max()
    plt.ylim(0, max_val * 1.1)
    
    # Garantir que o eixo X mostre todas as datas ordenadas
    plt.xlim(df_evolucao['mes_ano_dt'].min(), df_evolucao['mes_ano_dt'].max())
    
    plt.tight_layout()
    plt.savefig('evolucao_mensal.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. DISTRIBUIÇÃO DE FILMES x SÉRIES
    query_distribuicao = """
    SELECT type, COUNT(*) as quantidade
    FROM titles_clean
    GROUP BY type;
    """
    df_distribuicao = pd.read_sql(query_distribuicao, conn)
    
    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff']
    plt.pie(df_distribuicao['quantidade'], 
            labels=df_distribuicao['type'], 
            autopct='%1.1f%%', 
            startangle=90,
            colors=colors,
            textprops={'fontsize': 12})
    plt.title('Distribuição de Filmes vs Séries na Netflix', fontsize=14, fontweight='bold')
    plt.savefig('distribuicao_tipo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. ANÁLISE DE ELENCO - TOP ATORES
    query_elenco = """
    SELECT actor, COUNT(*) as quantidade
    FROM cast
    GROUP BY actor
    ORDER BY quantidade DESC
    LIMIT 20;
    """
    df_elenco = pd.read_sql(query_elenco, conn)
    
    plt.figure(figsize=(12, 10))
    bars = plt.barh(df_elenco['actor'], df_elenco['quantidade'], color='lightcoral')
    plt.xlabel('Número de Títulos', fontsize=12, fontweight='bold')
    plt.title('Top 20 Atores Mais Frequentes na Netflix', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('top_atores.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. ANÁLISE DE RATING (CLASSIFICAÇÃO ETÁRIA)
    query_rating = """
    SELECT rating, COUNT(*) as quantidade
    FROM titles_clean
    WHERE rating IS NOT NULL AND rating != 'not_rated'
    GROUP BY rating
    ORDER BY quantidade DESC;
    """
    df_rating = pd.read_sql(query_rating, conn)
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df_rating['rating'], df_rating['quantidade'], color='lightgreen')
    plt.xlabel('Classificação Etária', fontsize=12, fontweight='bold')
    plt.ylabel('Número de Títulos', fontsize=12, fontweight='bold')
    plt.title('Distribuição por Classificação Etária', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('distribuicao_rating.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 6. ANÁLISE ADICIONAL: GÊNEROS MAIS POPULARES
    query_generos = """
    SELECT genre, COUNT(*) as quantidade
    FROM titles_by_genre
    GROUP BY genre
    ORDER BY quantidade DESC
    LIMIT 15;
    """
    df_generos = pd.read_sql(query_generos, conn)
    
    plt.figure(figsize=(12, 10))
    bars = plt.barh(df_generos['genre'], df_generos['quantidade'], color='orange')
    plt.xlabel('Número de Títulos', fontsize=12, fontweight='bold')
    plt.title('Top 15 Gêneros na Netflix', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('top_generos.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 7. ANÁLISE ADICIONAL: DURAÇÃO DE FILMES
    query_duracao = """
    SELECT duration_value, COUNT(*) as quantidade
    FROM titles_clean
    WHERE type = 'Movie' AND duration_value IS NOT NULL AND duration_value <= 300
    GROUP BY duration_value
    ORDER BY duration_value;
    """
    df_duracao = pd.read_sql(query_duracao, conn)
    
    plt.figure(figsize=(12, 8))
    plt.hist(df_duracao['duration_value'], bins=30, alpha=0.7, 
             edgecolor='black', color='purple')
    plt.xlabel('Duração (minutos)', fontsize=12, fontweight='bold')
    plt.ylabel('Número de Filmes', fontsize=12, fontweight='bold')
    plt.title('Distribuição de Duração dos Filmes', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('distribuicao_duracao.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    conn.close()
    
    print("✅ Visualizações criadas com sucesso!")
    return True

# Executar análise
if __name__ == "__main__":
    create_visualizations()