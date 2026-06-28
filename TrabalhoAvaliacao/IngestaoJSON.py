print('''
# ============================================ #
#    Simulando a ingestao de dados via JSON
# ============================================ #
      ''')

# ===========================================
# 1 - Importando bibliotecas usadas nesta etapa
# ===========================================

import json, random, os
from datetime import datetime, timedelta

# ===========================================
# 2 - Criando uma pasta para execucao em qualquer ambiente
# ===========================================
PASTA_BRONZE_JSON = "data_lakehouse/bronze"
os.makedirs(PASTA_BRONZE_JSON, exist_ok = True)

# ===========================================
# 3 - Definindo uma lista para guardar os dados simulados das mensagens dos sensores
# ===========================================
baseDadosIoT = []

# Funcao para gerar uma data de forma aleatoria
def gerarData():
      data_inicio = datetime(2026, 1, 1)
      dia = random.randint(1, 150)

      # Dependendo do retorno da funcao random, a variavel hora, recebera um valor, pensando num cenario de pico ou entrepico na carga 
      if random.random() < 0.70:
            hora = random.choice([0, 1, 2, 3, 4, 10, 11, 12, 13])
      else:
            hora = random.choice([5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
      
      minuto = random.randint(1, 59)
      segundo = random.randint(0, 59)
      data_escolhida = data_inicio + timedelta(days = dia, hours = hora, minutes = minuto, seconds = segundo)

      return data_escolhida

# Estrutura de Repeticao para alimentar o dict que vai receber todos os dados dos sensores
for i in range (1, 5001):
    idEventoIoT = f"EVENTO_IOT_{i}"

    # Dados vindos dos sensores
    corrente = round(random.uniform(10.0, 32.0), 2) # Corrente
    tensao = random.choice([560, 600, 750, None]) # Tensao em Volts
    estado_carga = random.randint(0, 99) # Carga do Veiculo

    numero_eletroposto = random.randint(1, 500)
    idEletroposto = f"ELETRO_{numero_eletroposto}"

    data_carga = gerarData()
    data_carga_formatada = data_carga.strftime("%Y-%m-%d %H:%M:%S")

    # Definindo um dict com os dados gerados de forma aleatoria dos sensores para salvar cada evento de forma unica
    evento_IoT = {
        "IDEventoIoT": idEventoIoT,
        "IDEletroposto": idEletroposto,
        "TempoCarga": data_carga_formatada,
        "DadosSensores": { 
            "CorrenteEletroposto": corrente,
            "TensaoEletroposto": tensao,
            "CargaVeiculo": estado_carga
        } 
    }
    baseDadosIoT.append(evento_IoT)
    

# Salvando o dict no formato JSON para preservar os dados brutos (Camada Bronze)
caminho_arquivo = os.path.join(PASTA_BRONZE_JSON, "DadosSensores.json")
with open(caminho_arquivo, "w", encoding = "utf-8") as arquivo:
    json.dump(baseDadosIoT, arquivo, indent = 4, ensure_ascii=False)

print("Dados Gerados e Salvos Com Sucesso!")
