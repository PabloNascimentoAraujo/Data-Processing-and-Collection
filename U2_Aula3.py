# Video Aula VII - Unidade III 19.05.26 19h46
# Integracao com banco de dados
# Coleta de tipos diferentes bancos de dados e integrar tudo em um unico lugar

import sqlite3
import pandas as pd
import json

# -- 1. Simulando SQL
# Criando um banco de dados em memória e inserindo vendas
conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE vendas_sql (id INT, produto TEXT, valor REAL)')
conn.execute('INSERT INTO vendas_sql VALUES (1, "Notebook", 5000.00), (2, "Mouse", 150.00)')

# Ingestão de SQL via pandas
df_sql = pd.read_sql_query(sql='SELECT * FROM vendas_sql', con=conn)

# -- 2. Simulando NoSQL (MongoDB)
# Dados que viriam de um banco de documentos
nosql_docs = [
    {"id": 3, "item": "Teclado Mechanical", "preco": 300.00, "detalhes": {"cor": "RGB"}},
    {"id": 4, "item": "Monitor 4K", "preco": 2500.00, "garantia": "2 anos"}
]

# Ingestao NoSQL (Normalizando o JSON para tabela)
df_nosql = pd.json_normalize(nosql_docs)

# Ajustando nomes de colunas para baterem com o SQL
df_nosql = df_nosql.rename(columns = {'item': 'produto', 'preco': 'valor'})

# 3. Integracao analítica
# Unindo as duas fontes em um unico DataFrame (Data Lakehouse)
df_final = pd.concat(objs = [df_sql, df_nosql[['id', 'produto', 'valor']]], ignore_index = True)

# Resumo Analítico
print("### Relatório Consolidado (SQL + NoSQL) ###")
print(df_final)
print(f'\nTotal de Vendas Integradas: R$ {df_final['valor'].sum():.2f}')

