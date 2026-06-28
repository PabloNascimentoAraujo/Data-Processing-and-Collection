# 04.05.2026 - 20H45
# Video Aula 4 - Web Scraping com Python: Extracao de Dados, Ética e Aplicacoes no Mercado
# Web Scraping: extracao de dados diretamente de paginas da web. 
# Ferramentas do Python: requests e BeautifulSoup

import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Ci%C3%AAncia_de_dados"

try:
    print("Conectando ao site para extrair o resumo...")
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(url, headers=headers, timeout=10)

    if resposta.status_code == 200:
        sopa = BeautifulSoup(resposta.text, features="html.parser")

        # Comando find com p, captura a primeira ocorrencia de paragrafo:
        primeiro_paragrafo = sopa.find("p")

        if primeiro_paragrafo:
            texto_limpo = primeiro_paragrafo.get_text().strip()
            print("-" * 150)
            print("Primeiro paragrafo coletado")
            print(texto_limpo)
            print("-" * 150)
        else:
            print("Não foi possível encontrar nenhum paragrafo (<p> nesta pagina).")
    else:
        print(f"Erro de conexão: Status {resposta.status_code}.")
except Exception as e:
    print(f"Erro inesperado: {e}.")

