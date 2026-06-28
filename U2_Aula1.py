# 18.05.2026 - 19h44
# Video Aula 5 - Unidade II
# Formas de Ingestão de Dados - batch (lote), streaming (em tempo real), incremental(envia
# somente o que atualizou)

import time
import requests
import re
from bs4 import BeautifulSoup

# Funcoes de ingestao
def ingestao_batch(dados):
    print(f'\n--- [BATCH] Iniciando o processamento de {len(dados)} registros.')
    total = sum(d['valor'] for d in dados)
    print(f'Sucesso: R$ {total} processados em lote')

def ingestao_incremental(dados_db, ultimo_id_lido):
    print(f"\n--- [INCREMENTAL] Buscando novos dados após ID {ultimo_id_lido} ---")
    novos_dados = [d for d in dados_db if d['id'] > ultimo_id_lido]

    if novos_dados:
        for dado in novos_dados:
            print(f"Processando registro novo: {dado['id']}.")
        return novos_dados[-1]['id']
    else:
        print(f"Nenhum dado encontrado.")
        return ultimo_id_lido
    
def verificar_preco():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    headers = {"User-Agent": "Mozilla/5.0"}

    try: 
        resposta = requests.get(url, headers = headers, timeout = 10)
        sopa = BeautifulSoup(resposta.text, features = 'html.parser')

        nome_produto = sopa.find('h1').get_text()
        preco_texto = sopa.find('p', class_= "price_color").get_text() 


        preco_limpo = re.sub(r'[^\d.]','', preco_texto)
        preco_atual = float(preco_limpo)

        print(f"Produto: {nome_produto} | Preco: {preco_atual}.")

        if preco_atual < 52.00:
            print("O preco está abaixo da meta!!")

    except Exception as e:
        print(f"Erro na coleta ou limpeza: {e}.")

# Execucao
print("Iniciando monitoramento corrigido...")
for i in range(3):
    verificar_preco()
    time.sleep(5)