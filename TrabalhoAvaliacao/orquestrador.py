# Importando as bibliotecas necessárias
import time
import subprocess
import sys
import os

DIR = "data_lakehouse"
PASTA_BRONZE = os.path.join(DIR, "bronze")
PASTA_PRATA = os.path.join(DIR, "prata")
PASTA_OURO = os.path.join(DIR, "ouro")

def executar_script(script):
    if not os.path.exists(script):
        print(f"Arquivo {script} não localizado.")
        return False
    
    print(f"Iniciando a execucao do script: {script}.")
    inicio = time.time()

    try: 
        resultado = subprocess.run([sys.executable, script], capture_output = False, text = True)
        duracao_execucao = time.time() - inicio
        if resultado.returncode == 0:
            print(f"{script} concluído com sucesso em {duracao_execucao:.2f} segundos.")
            return True
        else:
            print(f"Erro ao executar o script {script}.")
            return False
    except Exception as e:
        print(f"Erro ao tentar executar o script {script}.")
        return False
    
def rodar_pipeline_completo():
    print("--- Iniciando pipeline - Lumina Energy --- ")
    
    # Sequencia da Arquitetura Medalhao - Camada Bronze
    print("--- Camada Bronze --- \n")
    sucesso_api = executar_script(os.path.join(PASTA_BRONZE, "IngestaoAPI.py"))
    sucesso_json = executar_script(os.path.join(PASTA_BRONZE, "IngestaoJSON.py"))
    sucesso_sql = executar_script(os.path.join(PASTA_BRONZE, "IngestaoSQL.py"))

    if not sucesso_api or not sucesso_json or not sucesso_sql:
        print("Dados essenciais falharam na Camada Bronze")
        return False
    else:
        print("Simulacao de Ingestao de Dados Completada com Sucesso!\n")

    # Camada Prata
    print("--- Camada Prata ---\n")
    if not executar_script(os.path.join(PASTA_PRATA, "Tratamento.py")):
        print("Falha no processamento da camada Prata.")
        return False
    else:
        print("Tratamento, Limpeza e Analise de Sentimento feitos com Sucesso!")

    # Camada Ouro
    print("--- Camada Ouro ---\n")
    if not executar_script(os.path.join(PASTA_OURO, "FatoDimensao.py")):
        print("Falha na camada Ouro")
        return False
    else:
        print("Construcao da Tabela Fato feita com Sucesso!")
        print("Data Lakehouse atualizado com sucesso!")
        return True
    
if __name__ == "__main__":
    INTERVALO = 20

    print(f"Orquestrador Ativo. Intervalo: {INTERVALO} segundos.")

    try: 
        while True:
            sucesso_pipeline = rodar_pipeline_completo()
            if sucesso_pipeline:
                print("Pipeline executado com exito.")
                break # Para nao iniciar uma nova execucao.
            else:
                print(f"Falha em alguma etapa do pipeline. Aguardando proxima janela de {INTERVALO} segundos")
                time.sleep(INTERVALO)
    except KeyboardInterrupt:
        print("Orquestrador encerrado pelo usuário.")
    except Exception as e:
        print(f"\n[Erro Fatal]: {e}")