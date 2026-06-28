
# =========================================================
# 1 - Importando as bibliotecas necessárias
# =========================================================
import os
import pandas as pd

# =========================================================
# 2 - Configurando os caminhos
# =========================================================
PASTA_PRATA = "data_lakehouse/prata"
PASTA_OURO = "data_lakehouse/ouro"
os.makedirs(PASTA_OURO, exist_ok = True)

print("Iniciando Processamento na Camada Ouro (Analytics)...\n")

# =======================================================================
# 3 - Carregando os dados dos textos vindos das redes sociais e Noticias
# =======================================================================
print("Carregando os dados dos textos tratados na camada anterior... ")
caminho_fontes = os.path.join(PASTA_PRATA, "FontesExternas.parquet")
df_fontes_externas = pd.read_parquet(caminho_fontes)

# Criando mais um campo no DataFrame para permitir o JOIN com os dados dos sensores
df_fontes_externas["DataDia"] = df_fontes_externas["data_evento"].dt.date

# Enviando o resultado da analise de sentimento
df_sentimento_dia = df_fontes_externas.groupby("DataDia")["ScoreSentimento"].mean().reset_index().round(2)


# ===============================================================
# 4 - Carregando os dados dos sensores e os dados de faturamento
# ===============================================================
print("Carregando os dados dos sensores e do faturamento oriundos da camada prata.")
df_iot = pd.read_parquet(os.path.join(PASTA_PRATA, "iotSensoresPrata.parquet"))
df_faturamento = pd.read_parquet(os.path.join(PASTA_PRATA, "faturamentoPrata.parquet"))

# Convertendo os campos para datetime antes de arredondar.
df_iot["TempoCarga"] = pd.to_datetime(df_iot["TempoCarga"])
df_faturamento["DataTransacao"] = pd.to_datetime(df_faturamento["DataTransacao"])

# Campo de Data para cruzar com os dados dos sensores
df_iot["DataHora"] = df_iot["TempoCarga"].dt.round("h")
df_iot["DataDia"] = df_iot["TempoCarga"].dt.date
df_faturamento["DataHora"] = df_faturamento["DataTransacao"].dt.round("h")

# Garantindo homogeneidade total nos tipos das chaves de merge
df_iot["DataHora"] = pd.to_datetime(df_iot["DataHora"])
df_faturamento["DataHora"] = pd.to_datetime(df_faturamento["DataHora"])

# ===============================================================
# 5 - Prevenindo a duplicidade na Camada Financeira
# ===============================================================
df_fat_agrupado = df_faturamento.groupby([ "IDEletroposto", "IDCliente"]).agg({
    "ValorPagamento": "sum" 
}).reset_index()

# ===============================================================
# 6 - Novo DataFrame para cruzar o cliente com o posto, removendo registros duplicados
# ===============================================================

df_cliente_posto = df_fat_agrupado.drop_duplicates(subset = ["IDEletroposto"])[["IDEletroposto", "IDCliente"]]


# ===============================================================
# 7 - Construindo a tabela Fato
# ===============================================================
print("Construcao da Tabela Fato...\n")

# Unindo, o que foi registrado nos sensores e enviado via IoT, com o sentimento de mercado
df_fato = pd.merge(df_iot, df_sentimento_dia, on = "DataDia", how = "left")

# Salvando o preenchimento de valores nulos
df_fato["ScoreSentimento"] = df_fato["ScoreSentimento"].fillna(0.0) 

# Remover a coluna auxiliar de data para manter o arquivo limpo
df_fato = df_fato.drop(columns=["DataDia"])

# Segundo Merge
df_fato = pd.merge(df_fato, df_cliente_posto, on = ["IDEletroposto"], how = "left")

# Caso nao tiver um faturamento atrelado a um cliente na mesma hora
df_fato["IDCliente"] = df_fato["IDCliente"].fillna("CLIENTE_DESCONHECIDO")

# Terceiro Merge: Traz o valor do faturamento associado à combinação Posto + Cliente
df_fato = pd.merge(df_fato, df_fat_agrupado, on = ["IDEletroposto", "IDCliente"], how = "left")

# Enviando um valor padrao caso nao seja encontrada uma transacao financeira para o evento do sensor
df_fato["ValorPagamento"] = df_fato["ValorPagamento"].fillna(0.0)

# Calculando a demanda energetica total da leitura
df_fato["DemandaPotencia_kW"] = (df_fato["Corrente(A)"] * df_fato["Tensao(V)"]) / 1000
df_fato["DemandaPotencia_kW"] = df_fato["DemandaPotencia_kW"].round(2)

# ===============================================================
# 8 - Salvando o resultado do processamento acima na camada Ouro
# ===============================================================
caminho_fato_recarga = os.path.join(PASTA_OURO, "fatoRecarga.parquet")
df_fato.to_parquet(caminho_fato_recarga, index = False)

print("\nCamada Ouro gerada...")
print(f"Tabela Fato salva em: {caminho_fato_recarga}.")
print(f"Total de Registros prontos para o Dashboard: {len(df_fato)} linhas.")
