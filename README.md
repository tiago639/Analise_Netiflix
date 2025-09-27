#🎬 Projeto de Análise de Dados da Netflix
📌 Objetivo

Este projeto tem como objetivo aplicar um processo de ETL (Extract, Transform, Load) em dados da Netflix, armazená-los em um banco de dados relacional, realizar consultas em SQL, processar dados com Python, e por fim construir um dashboard interativo no Power BI para análise de insights.

🛠️ Ferramentas Necessárias

Antes de rodar o projeto, instale/configure os seguintes softwares:

Python 3.9+

Bibliotecas necessárias (instale com pip install -r python_etl/requirements.txt)

pandas, sqlite3, matplotlib, seaborn

SQLite
 (ou use o DB Browser for SQLite)

Power BI Desktop
 (para abrir e editar o dashboard, caso queira)

Git
 (para clonar o repositório e versionar o projeto)

📂 Estrutura do Repositório
📦 Analise_Netflix
 ┣ 📂 data
 ┃ ┗ netflix_titles.csv        # Dataset original
 ┣ 📂 python_etl
 ┃ ┣ etl_netflix.py            # Script principal do ETL
 ┃ ┣ Aanlise.py                # Script auxiliar de análise
 ┃ ┗ requirements.txt          # Dependências do Python
 ┣ 📂 sql_scripts
 ┃ ┣ create_tables.sql         # Criação de tabelas intermediárias
 ┃ ┣ insert_data.sql           # Inserção de dados
 ┃ ┗ transformations.sql       # Consultas e transformações
 ┣ 📂 powerbi
 ┃ ┣ dashboard_screenshots/    # Prints do dashboard
 ┃ ┣ dashboard_description.md  # Documentação do dashboard
 ┃ ┗ Netflix Dashboard.pbix    # Arquivo editável do Power BI (opcional)
 ┣ 📂 docs
 ┃ ┗ Documentacao_Projeto_Netflix.docx  # Documentação detalhada em Word
 ┣ 📂 outputs
 ┃ ┣ netflix.db                # Banco SQLite gerado
 ┃ ┣ distribucao_tipo.png      # Gráficos gerados
 ┃ ┣ top_paises.png
 ┃ ┣ top_generos.png
 ┃ ┣ top_atores.png
 ┃ ┗ evolucao_mensal.png
 ┣ README.md                   # Documentação principal

🚀 Como Executar
1️⃣ Clonar o repositório
git clone https://github.com/tiago639/Analise_Netiflix.git
cd Analise_Netiflix

2️⃣ Criar ambiente Python e instalar dependências
cd python_etl
pip install -r requirements.txt

3️⃣ Executar o ETL
python etl_netflix.py


👉 Isso vai:

Ler o dataset netflix_titles.csv

Limpar e transformar os dados

Gerar o banco netflix.db com as tabelas intermediárias

4️⃣ Consultar no SQLite

Abra o arquivo sql_scripts/create_tables.sql no DB Browser for SQLite ou no terminal:

sqlite3 netflix.db < sql_scripts/create_tables.sql

5️⃣ Abrir o Dashboard no Power BI

Abra powerbi/Netflix Dashboard.pbix no Power BI Desktop

Ou visualize os prints na pasta powerbi/dashboard_screenshots

📊 Dashboard

O dashboard contém análises como:

Evolução de lançamentos ao longo do tempo

Distribuição de títulos por tipo (Filme x Série)

Principais países produtores

Gêneros mais populares

Top atores/diretores recorrentes


📈 Conclusões

A Netflix teve um crescimento expressivo de lançamentos após 2015, com pico em 2019.

Os EUA e Índia dominam a produção de conteúdo.

Filmes ainda são maioria no catálogo em relação às séries.

Dramas e Documentários aparecem como os gêneros mais recorrentes.

