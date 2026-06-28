# Arquivo para tratamento do que foi coletado nas tres fontes de dados

# Importando as bibliotecas
import os, json
import pandas as pd

# Configurando os caminhos
PASTA_BRONZE = "data_lakehouse/bronze"
PASTA_PRATA = "data_lakehouse/prata"
os.makedirs(PASTA_PRATA, exist_ok = True)

print("--- Iniciando Processamento na Camada Prata ---\n")

# ================================================================
# Tratamento dos Dados de Faturamento
# ================================================================

# Tratamento dos dados de Faturamento
print("Processando dados de faturamento... \n")

# Lendo o CSV Bruto
df_faturamento_bruto = pd.read_csv(os.path.join(PASTA_BRONZE, "baseFaturamentoBruto.csv"), sep = ";")

# Convertendo os campos de data para o formato datetime
df_faturamento_bruto["DataLogCdc"] = pd.to_datetime(df_faturamento_bruto["DataLogCdc"])
df_faturamento_bruto["DataTransacao"] = pd.to_datetime(df_faturamento_bruto["DataTransacao"])

# Aplicando o CDC ordenando os eventos por data do log
df_fat_prata = df_faturamento_bruto.sort_values(by = "DataLogCdc", ascending = True)

# Removendo o que é duplicado, exceto a última ocorrencia
df_fat_prata = df_fat_prata.drop_duplicates(subset = ["IDFaturamento"], keep = "last")

# Removendo a coluna que descreve a operacao do CDC
df_fat_prata = df_fat_prata.drop(columns = ["Op"])

# Salvando um arquivo no formato parquet, após as tratativas básicas
df_fat_prata.to_parquet(os.path.join(PASTA_PRATA, "faturamentoPrata.parquet"), index = False)
print("Dados de faturamento processados... \n")

# ================================================================
# Tratamento dos Dados dos Eletropostos e dos Clientes
# ================================================================
print("Processando os dados dos Eletropostos e dos Clientes...\n")

# Lendo os CSVs brutos
df_eletroposto_bruto = pd.read_csv(os.path.join(PASTA_BRONZE, "baseEletropostosBrutos.csv"), sep = ";")
df_cliente_bruto = pd.read_csv(os.path.join(PASTA_BRONZE, "baseClientesBrutos.csv"), sep = ";")

# Padronizando os textos e fazendo limpeza básica
df_eletroposto_bruto["EnderecoCompletoEletroposto"] = df_eletroposto_bruto["EnderecoCompletoEletroposto"].str.title()
df_cliente_bruto["NomeCliente"] = df_cliente_bruto["NomeCliente"].str.title()

# Salvando um arquivo no formato parquet, após as tratativas básicas
df_eletroposto_bruto.to_parquet(os.path.join(PASTA_PRATA, "eletropostoPrata.parquet"), index = False)
df_cliente_bruto.to_parquet(os.path.join(PASTA_PRATA, "clientePrata.parquet"), index = False)
print("Dados dos Clientes e dos Eletropostos processados...\n")

# =================================================
# Tratamento de Dados dos Sensores
# =================================================
print("Processando dados dos sensores IoT...\n")

# Lendo os dados do arquivo JSON
with open(os.path.join(PASTA_BRONZE, "DadosSensores.json"), "r", encoding = "utf-8") as arquivo:
    dados_iot_bruto = json.load(arquivo)

# Convertendo o resultado da leitura do arquivo para um objeto do tipo DataFrame
df_iot_bruto = pd.DataFrame(dados_iot_bruto)

# Criando novas colunas a partir dos pares chave-valor existentes em DadosSensores
df_iot_bruto["Corrente(A)"] = df_iot_bruto["DadosSensores"].apply(lambda x: x["CorrenteEletroposto"])
df_iot_bruto["Tensao(V)"] = df_iot_bruto["DadosSensores"].apply(lambda x: x["TensaoEletroposto"])
df_iot_bruto["SoC(%)"] = df_iot_bruto["DadosSensores"].apply(lambda x: x["CargaVeiculo"])

# Removendo do DataFrame a coluna aninhada
df_iot_prata = df_iot_bruto.drop(columns = ["DadosSensores"])

# Convertendo a data para DateTime
df_iot_prata["TempoCarga"] = pd.to_datetime(df_iot_prata["TempoCarga"])

# Tratando os dados nulos
df_iot_prata["Tensao(V)"] = df_iot_prata.groupby("IDEletroposto")["Tensao(V)"].transform(lambda x: x.fillna(x.median()))

# Preenchendo algum valor restante com o valor padrao: 220V
df_iot_prata["Tensao(V)"] = df_iot_prata["Tensao(V)"].fillna(750)

# Salvando o arquivo parquet apos as transformacoes
df_iot_prata.to_parquet(os.path.join(PASTA_PRATA, "iotSensoresPrata.parquet"), index = False)


# =================================================
# Tratamento de Dados das fontes externas
# =================================================
# Leitura das 3 fontes
df_noticias = pd.read_json(os.path.join(PASTA_BRONZE, "NoticiasBruto.json"))
df_redes = pd.read_json(os.path.join(PASTA_BRONZE, "RedesSociaisBruto.json"))
df_scraping = pd.read_json(os.path.join(PASTA_BRONZE, "ScrapingBruto.json"))

# Padronizando todas as colunas
df_noticias_colunas_padrao = df_noticias.rename(columns = {
    "DataPublicacao": "data_evento",
    "Manchete": "texto_bruto",
    "Fonte": "origem"
})[["data_evento", "texto_bruto", "origem"]]

df_redes_colunas_padrao = df_redes.rename(columns = {
    "DataPostagem": "data_evento",
    "TextoPost": "texto_bruto",
    "Plataforma": "origem"
})[["data_evento", "texto_bruto", "origem"]]

df_scraping_colunas_padrao = df_scraping.rename(columns = {
    "DataColeta": "data_evento",
    "HTMLBruto": "texto_bruto",
    "SiteOrigem": "origem"
})[["data_evento", "texto_bruto", "origem"]]


# Unificando todos os DataFrames de fontes externas em um só.
df_unificado = pd.concat([df_noticias_colunas_padrao, df_redes_colunas_padrao, df_scraping_colunas_padrao], ignore_index = True)

# Convertendo o campo de data para o tipo datetime
df_unificado["data_evento"] = pd.to_datetime(df_unificado["data_evento"])

# Removendo quebras de linhas do campo que recebe o texto maior
df_unificado["texto_bruto"] = df_unificado["texto_bruto"].str.replace(r"\s", " ", regex = True).str.strip()

# Análise de Sentimento e Salvando o ScoreSentimento na Camada Prata
def gerarPontuacao(texto):
    import random
    from textblob import TextBlob

    # Carregando o resultado da chamada da funcao TextBlob no objeto analise
    analise = TextBlob(texto)
    score_textblob = analise.sentiment.polarity

    # Palavras de parametro para medir a pontuacao
    palavras_positivas = [
        "expansão", "sucesso", "zera", "recorde", "bater", "satisfação", 
        "elogiou", "celebrando", "limpa", "rápido", "adorou", "parabéns", 
        "parceria", "reduz", "bônus", "eficiência", "estabilidade", "reduziu", 
        "vantagem", "sustentabilidade", "inovação", "melhorou", "sensacional", "lucro"
    ]
   
    palavras_negativas = [
        "apagão", "falha", "queima", "protestam", "abusivo", "sobrecarrega", 
        "reajuste", "quebrada", "péssimo", "erro", "absurdo", "crise", 
        "severo", "paralisa", "crônica", "aumento", "duplicadas", "procon", 
        "gargalos", "graves", "riscos", "reclamação", "vergonha", "vulnerabilidade"
    ]

    score_final = score_textblob

    texto_lower = texto.lower()
    for p in palavras_positivas:
        if p in texto_lower:
            score_final += 0.25
    for p in palavras_negativas:
        if p in texto_lower:
            score_final -= 0.25

    # Aplicando um valor caso o score_final saia da verificacao acima zerado
    if round(score_final, 2) == 0.0:
        score_final = random.choice([random.uniform(-0.15, -0.02), random.uniform(0.02, 0.15)])

    return round(max(min(score_final, 1.0), -1.0), 2)

print("Executando a analise de sentimento...\n")
df_unificado["ScoreSentimento"] = df_unificado["texto_bruto"].apply(gerarPontuacao)


# Salvando no formato parquet
df_unificado.to_parquet(os.path.join(PASTA_PRATA, "FontesExternas.parquet"), index = False)

print(f"Score de Sentimento Gerado. Dados limpos e armazenados em {PASTA_PRATA}. ")
