# 04.05.2026 - 19h51
# Video Aula 2 - Coleta e Transformacao de Dados: Fontes, Métodos e Aplicacoes Estrategicas
# Código em Python organizar dados de fontes internas e externas
# Consultar Banco de Dados, APIs, sensores, web.

# Simulacao de Coleta de Dados brutos (pode vir de um sensor ou texto web)
import pandas as pd
dados_brutos = [
    "ID: 101, Sensor: Temperatura, Valor: 25.5",
    "ID: 102, Sensor: Umidade, Valor: 60"
]

# Processamento e Limpeza para transformar em dado estruturado
registros = []

for item in dados_brutos:
    # Extraindo os valores após os dois pontos
    valores = [v.split(": ")[1] for v in item.split(", ")]
    registros.append(valores)

# Criando o DataFrame
df = pd.DataFrame(registros, columns=["ID", "Tipo_Sensor", "Leitura"])

# Carga (Ingestão) para um arquivo csv estruturado
df.to_csv(path_or_buf="coleta_sensores.csv", index=False)