# ===========================================
# 1 - Importando as bibliotecas necessarias
# ===========================================
import random, os
import pandas as pd
from datetime import datetime, timedelta

# ===========================================
# 2 - Criando uma pasta para execucao em qualquer ambiente
# ===========================================
PASTA_BRONZE_SQL = "data_lakehouse/bronze"
os.makedirs(PASTA_BRONZE_SQL, exist_ok = True)

# ==========================================================================================================
#  3 - Estruturas de Dados já alimentadas para auxilio na persistencia das listas de dicionarios principais
# ==========================================================================================================
# Listas usadas para persistir o dict baseDadosEletropostos
# Tipos de Logradouros
tipos_logradouro = ["Avenida", "Rua", "Alameda", "Praça", "Rodovia", "Travessa", "Estrada", "Vila", "Beco", "Passagem"]

# Nomes dos Logradouros
nomes_logradouro = ["Volta Redonda", "Santos Dumont", "Nikola Tesla", "Thomas Edison", "Michael Faraday",
"James Watt", "Benjamin Franklin", "Alessandro Volta", "André Ampère", "Georg Ohm", "da Paz", "da Alvorada", 
"Sete de Setembro", "Quinze de Novembro", "Treze de Maio",
"Tiradentes", "Princesa Isabel", "Duque de Caxias", "Castro Alves", "Machado de Assis",
"Clarice Lispector", "Carlos Drummond", "Cecília Meireles", "Erico Verissimo", "Ariano Suassuna",
"Jorge Amado", "Monteiro Lobato", "Anita Garibaldi", "Zumbi dos Palmares", "Aleijadinho",
"Tarsila do Amaral", "Candido Portinari", "Oscar Niemeyer", "Tom Jobim", "Chico Buarque",
"Elis Regina", "Milton Nascimento", "Caetano Veloso", "Gilberto Gil", "Pixinguinha",
"dos Pinheiros", "das Palmeiras", "das Orquídeas", "dos Girassóis", "das Nações",
"do Progresso", "da Inovação", "da Sustentabilidade", "do Futuro", "Central"]

# Bairros Ficticios
bairros_porto_real = [
    "Centro Histórico", "Jardim Oceânico", "Vila Elétrica", "Alto da Colina", "Porto Novo",
    "Bairro das Nações", "Distrito Industrial", "Parque Tecnológico", "Bela Vista", "Mirante do Sol",
    "Vale Verde", "Novo Horizonte", "Jardim Botânico", "Praia das Conchas", "Estação Central",
    "Aeroporto", "Boavista", "Santa Teresa", "Vila Nova", "Cidade Alta",
    "Ribeirão Preto", "Portal do Vale", "São João", "Santo Antônio", "Alphaville Real"]

# Listas e Lista de Dicionarios para persistir o dict baseDadosClientes
# Lista com 100 nomes completos de clientes (Simulação SQL)
nomes_clientes = ["Ana Silva", "Bruno Santos", "Carlos Oliveira", "Daniela Souza", "Eduardo Lima",
"Fernanda Pereira", "Gabriel Costa", "Amanda Rodrigues", "Igor Almeida", "Juliana Nascimento",
"Lucas Ribeiro", "Mariana Carvalho", "Pedro Gomes", "Renata Martins", "Thiago Rocha",
"Vanessa Ribeiro", "Rodrigo Alves", "Camila Araujo", "Diego Melo", "Larissa Cruz",
"Fabio Reis", "Leticia Dias", "Gustavo Novaes", "Beatriz Ramos", "Leandro Ferreira",
"Carolina Barbosa", "Marcelo Vieira", "Aline Teixeira", "Ricardo Cardoso", "Patricia Machado",
"Marcos Neves", "Priscila Freire", "Roberto Souza", "Danielle Moreira", "Otavio Castro",
"Tatiane Costa", "Samuel Lopes", "Monique Guimaraes", "Vitor Fonseca", "Sabrina Pires",
"Murilo Carvalho", "Bianca Cunha", "Arthur Resende", "Luana Farias", "Caio Antunes",
"Gabriela Mendes", "Felipe Nogueira", "Julia Diniz", "Rafael Assis", "Isabela Borges",
"Thiago Couto", "Manuela Campos", "Alexandre Duarte", "Giovanna Franco", "Leonardo Malta",
"Heloisa Viana", "Mauricio Quadros", "Larissa Prado", "Douglas Godoy", "Andreia Toledo",
"Rogerio Menezes", "Nathalia Rocha", "Cesar Paiva", "Thais Bicalho", "Jefferson Siqueira",
"Leticia Dornelas", "William Dorneles", "Jessica Azevedo", "Renan Junqueira", "Debora Dornas",
"Matheus Veras", "Stefany Meireles", "Ronaldo Goulart", "Kamila Bragança", "Wesley Aguiar",
"Mayara Sanches", "Denis Valente", "Priscila Lacerda", "Vinicius Peixoto", "Lorena Fontes",
"Allan Caldeira", "Talita Montenegro", "Patrick Sampaio", "Raissa Frota", "Erick Guerra",
"Nayara Villela", "Yago Sales", "Poliana Portela", "Ruan Beyer", "Milena Fagundes",
"Hiago Dorneles", "Paloma Lemos", "Caio Schimidt", "Viviane Dornas", "Fabricio Lourenço",
"Tania Maciel", "Geraldo Alencar", "Sonia Nazario", "Reinaldo Fraga", "Luiza Peçanha"]

# Dicionário/Lista com Fabricantes, Modelos e Especificações Técnicas (Tensão, Ano, etc.)
veiculos_eletricos = [
    {
        "fabricante": "BYD",
        "modelo": "D9W (Urbano Padron)",
        "ano_fabricacao_modelo": 2024,
        "tensao_max_suportada_v": 750
    },
    {
        "fabricante": "BYD",
        "modelo": "D11B (Articulado)",
        "ano_fabricacao_modelo": 2023,
        "tensao_max_suportada_v": 750
    },
    {
        "fabricante": "Mercedes-Benz",
        "modelo": "eO500U (Electro)",
        "ano_fabricacao_modelo": 2023,
        "tensao_max_suportada_v": 750
    },
    {
        "fabricante": "Volvo",
        "modelo": "BZL Electric",
        "ano_fabricacao_modelo": 2024,
        "tensao_max_suportada_v": 600
    },
    {
        "fabricante": "Eletra",
        "modelo": "e-Bus 12.1m (Chassi Scania/WEG)",
        "ano_fabricacao_modelo": 2024,
        "tensao_max_suportada_v": 650
    },
    {
        "fabricante": "Eletra",
        "modelo": "e-Bus 15m (Chassi Mercedes/WEG)",
        "ano_fabricacao_modelo": 2024,
        "tensao_max_suportada_v": 650
    },
    {
        "fabricante": "Marcopolo",
        "modelo": "Attivi Integral",
        "ano_fabricacao_modelo": 2023,
        "tensao_max_suportada_v": 650
    },
    {
        "fabricante": "Ankai",
        "modelo": "HFF6120G03EV (Urbano)",
        "ano_fabricacao_modelo": 2024,
        "tensao_max_suportada_v": 700
    }
]


# ==============================================
# 4 - Funcoes para Alimentar as listas principais
# ==============================================
# Eletroposto
def gerarEletroposto():
      baseDadosEletroposto = []
      for i in range(1, 501):
            posicoesRecarga = random.choice([1, 15])
            capacidadeMaxCarga = random.choice([600, 650, 700, 750])
            baseDadosEletroposto.append({
                "IDEletroposto": f"ELETRO_{i}",
                  "EnderecoCompletoEletroposto": f"{random.choice(tipos_logradouro)} {random.choice(nomes_logradouro)}, {random.choice(bairros_porto_real)} - Porto Real - Brasil",
                  "QtdePosicoesRecarga": posicoesRecarga,
                  "CapacidadeMaximaCarga": capacidadeMaxCarga
                  })
      return pd.DataFrame(baseDadosEletroposto)

# Gerando os dados de 100 clientes com seus respectivos veiculos
def gerarClientes():
    baseDadosClientes = []
    nomes_selecionados = random.sample(nomes_clientes, min(len(nomes_clientes), 100))
    for i, nome in enumerate(nomes_selecionados, 1):
            veiculo = random.choice(veiculos_eletricos)
            baseDadosClientes.append({
                "IDCliente": f"IDCliente_{i}",
                "NomeCliente": nome,
                "FabricanteVeiculo": veiculo["fabricante"],
                "ModeloVeiculo": veiculo["modelo"],
                "AnoFabricacaoVeiculo": veiculo["ano_fabricacao_modelo"],
                "TensaoMaxima": veiculo["tensao_max_suportada_v"]                  
            })
    return pd.DataFrame(baseDadosClientes)

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

def gerarFaturamento(df_eletropostos, df_clientes, qtdeTransacoes):
    baseFaturamento = []
    lista_eletropostos = df_eletropostos["IDEletroposto"].tolist()
    lista_clientes = df_clientes["IDCliente"].tolist()

    for i in range(1, qtdeTransacoes + 1):
        idFaturamento = f"FAT_{i}"
        idEletropostoEscolhido = random.choice(lista_eletropostos)
        idClienteEscolhido = random.choice(lista_clientes)

        data_primeiro_faturamento = gerarData()
        data_primeiro_faturamento_formatada = data_primeiro_faturamento.strftime("%Y-%m-%d %H:%M:%S")

        status_inicial = random.choice(["Pago", "Pendente"])
        valor_pago = round(random.uniform(30.0, 400.0), 2)

        # Operacao de Insert
        baseFaturamento.append({
             "Op": "INSERT",
             "DataLogCdc": data_primeiro_faturamento_formatada,
             "IDFaturamento": idFaturamento,
             "IDEletroposto": idEletropostoEscolhido,
             "IDCliente": idClienteEscolhido,
             "StatusPagamento": status_inicial,
             "ValorPagamento": valor_pago,
             "DataTransacao": data_primeiro_faturamento_formatada
        })

        # Operacao de Update - Atualizando uma transacao que possa estar como pendente, definindo que isso pode ocorrer com 80% de chance
        if status_inicial == "Pendente" and random.random() < 0.80:
             
            # Gerar uma data de liquidicao da transacao feita de 1 a 3 dias apos o inicio da transacao
            data_faturamento_atualizada = data_primeiro_faturamento + timedelta(days = random.randint(1, 3), hours = random.randint(0, 12))
            data_faturamento_final = data_faturamento_atualizada.strftime("%Y-%m-%d %H:%M:%S")

            # Atualizando a transacao
            baseFaturamento.append({
                 "Op": "UPDATE",
                 "DataLogCdc": data_faturamento_final,
                 "IDFaturamento": idFaturamento,
                 "IDEletroposto": idEletropostoEscolhido,
                 "IDCliente": idClienteEscolhido,
                 "StatusPagamento": random.choice(["Pago", "Cancelado"]),
                 "ValorPagamento": valor_pago,
                 "DataTransacao": data_primeiro_faturamento_formatada
            })

    return pd.DataFrame(baseFaturamento)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print('''# =================================================================================== #
# Iniciando a simulacao da ingestao de dados de faturamento feitos em um Banco de Dados Relacional
# =================================================================================== #
      ''')

    # Gerando os DataFrames resultantes de cada funcao
    df_eletropostos = gerarEletroposto()
    df_clientes = gerarClientes()
    df_faturamento = gerarFaturamento(df_eletropostos, df_clientes, qtdeTransacoes = 1000)

    # Caminho dos arquivos CSV
    caminho_eletropostos = os.path.join(PASTA_BRONZE_SQL, "baseEletropostosBrutos.csv")
    caminho_clientes = os.path.join(PASTA_BRONZE_SQL, "baseClientesBrutos.csv")
    caminho_faturamento = os.path.join(PASTA_BRONZE_SQL, "baseFaturamentoBruto.csv")

    # Salvando os DataFrames gerados por cada uma das funcoes
    df_eletropostos.to_csv(caminho_eletropostos, index = False, encoding = "utf-8", sep = ";")
    df_clientes.to_csv(caminho_clientes, index = False, encoding = "utf-8", sep = ";")
    df_faturamento.to_csv(caminho_faturamento, index = False, encoding = "utf-8", sep = ";")

    print("Tabelas de Cadastro e de Faturamento salvos com Sucesso.")
    print(f"Arquivos gerados em: {PASTA_BRONZE_SQL}")

    # Exibindo o DataFrame de Faturamento
    print("### Primeiros 5 registros da tabela de faturamento ###")
    print(df_faturamento[["Op", "DataLogCdc", "IDFaturamento", "IDEletroposto", "IDCliente", "StatusPagamento", "ValorPagamento"]].head(5))
    

     


     


