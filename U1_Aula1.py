# 04.05.2026 - 19h51
# Video aula 1 - Transformando Dados Brutos em Ativos Estratégicos
# Biblioteca Recomendada para operaćões essenciais
import pandas as pd

# 1 - Texto de origem - considerado dado não estruturado
texto_bruto = """
ID: 1, Produto: Teclado, Preco: 150
ID: 2, Produto: Mouse, Preco: 80
ID: 3, Produto: Monitor, Preco: 1300
ID: 4, Produto: Mesa, Preco: 900
ID: 5, Produto: Cadeira, Preco: 600
"""

# 2 - Extracao e transformacao (Processamento e Limpeza)
registros = []
for linha in texto_bruto.strip().split("\n"):
    partes = [p.split(": ") for p in linha.split(", ")]
    registros.append(partes)

# 3 - Criacao do DataFrame e gravacao no csv
colunas = ["ID", "Produto", "Preco"]
df = pd.DataFrame(registros, columns=colunas)

# Salva o arquivo csv (Ingestão e Armazenamento)
df.to_csv(path_or_buf="dados_extraidos.csv", index=False)

print(f"Arquivo gerado com sucesso!")




