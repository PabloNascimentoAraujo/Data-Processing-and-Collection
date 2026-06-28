# Video Aula 8 - Unidade II 19.05.26 20h17
# Coleta de dados de forma aleatoria, tratar os dados de forma rapida, deixando-os prontos para consulta, pesquisa e tomada de decisao
# Organizacao de Dados Brutos em um Data Lake
# Coleta de Dados via Scrapping

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# --- 1. COLETA ESTRATÉGICA (WEB SCRAPPING)
# Usando as bibliotecas Requests e BeautifulSoup

def coletar_dados_web():
    # Simulando a extracao de dados de um e-commerce
    # NA pratica, usaria requests.get(url)

    html_exemplo = """
    <html>
        <body>
            <div class="produto"> <span class="nome"> Smartphone X </span> <span class="preco"> R$ 2.500,00</span></div>
            <div class="produto"> <span class="nome"> Laptop X </span> <span class="preco"> R$ 12.500,00</span></div>
            <div class="produto"> <span class="nome"> Tablet Z X </span> <span class="preco"> R$ 900,00</span></div>
        </body>
    </html>
    """

    soup = BeautifulSoup(html_exemplo, features ='html.parser')
    dados_brutos = []

    for item in soup.find_all(name = 'div', class_= 'produto'):
        nome = item.find('span', class_ = 'nome').text
        preco = item.find('span', class_ = 'preco').text
        dados_brutos.append({'produto': nome, 'valor': preco})
    
    return dados_brutos

# --- 2. Camada Bronze (Raw Ingestion)
# Objetivo: manter uma tabela verdade historica com dados originais
def camada_bronze(dados):
    # Salvando os dados exatamente com vieram da fonte (formato original)
    with open('data_lake_bronze.json', 'w', encoding = 'utf-8') as f:
        json.dump(dados, f, ensure_ascii=False)
    print(f'>>> Camada Bronze: Dados Brutos ingeridos e armazenados.\n')
    return pd.DataFrame(dados)

# --- 3. Camada Prata (Filtered / Cleaned)
# Objetivo: Limpeza, filtragem e normalizacao para tornar os dados confiaveis
def camada_prata(df_bronze):
    df_silver = df_bronze.copy()

    # Normalizacao: Limpando a string do preco e convertendo para float
    df_silver['valor_numerico'] = df_silver['valor'].str.replace('R$', '', regex = False).str.replace('-', '', regex = False).str.replace(',', '.', regex = False) \
    .str.strip()

    # Tratamento de Erros: Removendo ou corrigindo valores nulos
    df_silver['valor_numerico'] = pd.to_numeric(df_silver['valor_numerico'], errors = 'coerce')
    df_silver = df_silver.dropna(subset = ['valor_numerico'])

    print(f'>>> Camada Prata: Dados Limpos, normalizados e validados.\n')
    return df_silver

# --- 4.. Camada Ouro (Business Agregate)
#  Objetivo: Agregados e metricas prontas para BI e tomada de decisao
def camada_ouro(df_silver):
    # Exemplo de Metrica de Negocio
    metricas_negocio = {
        "total_produto": [len(df_silver)],
        "ticket_medio": [df_silver['valor_numerico'].mean()],
        "valor_total_estoque": [df_silver['valor_numerico'].sum()]
    }

    # Transformando em um ativo valioso para analise
    df_gold = pd.DataFrame(metricas_negocio)
    print(">>> Camada Ouro: Metricas de Negocio Gerados com Sucesso !!\n")
    return df_gold
    

## -- Execucao do Pipeline
print("Iniciando Ciclo de inteligencia de dados... \n")

## Passo 1 - Web Scraping (Automacao com Python)
raw_data = coletar_dados_web()

## Passo 2 - Camada Bronze - Ingestao dos Dados Brutos
df_bronze = camada_bronze(raw_data)

# Passo 3 - Camada Prata - Limpeza e Transformacao
df_silver = camada_prata(df_bronze)

# Passo 4 - Camada Ouro - Dados prontos para tomada de decisao
df_gold = camada_ouro(df_silver)

print(df_gold)

 # Ainda nao funciona por completo!!
 # Arruma!!!