# 04.05.2026 - 20h16
# Video Aula 3 - Dados Semiestruturados e APIs REST: Integracao Segura entre sistemas
# Coleta de Dados via API - Acessando a API do IBGE

import requests
import pandas as pd

# URL da API do IBGE (Fonte Externa de Dados Semiestruturados)
url_api = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios"

try:
    print(f"Tentando coletar dados de: {url_api}.")

    # Adicionado um timeout de 15 segundos para dar tempo a conexao
    response = requests.get(url_api, timeout=15)

    # Em caso de resposta positiva, o dado bruto (JSON) será transformado em CSV
    if response.status_code == 200:
        dados_json = response.json()
        df = pd.DataFrame(dados_json)

        # Selecionando as colunas e salvando
        df_final = df[["id", "nome"]] # Colunas vindas do proprio site do IBGE
        df_final.to_csv("municipios_sp.csv", index=False, encoding="utf-8-sig")

        print("Coleta realizada com sucesso. Arquivo gerado.")

    else:
        print(f"O servidor respondeu, mas com erro: {response.status_code}.")

except requests.exceptions.ConnectTimeout:
    print("Erro: A conexão demorou muito tempo. Verifique a sua internet ou se há um firewall bloqueando o Python.")
except Exception as e:
    print(f"Erro inesperado: {e}.")