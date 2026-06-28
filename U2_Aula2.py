# Video Aula VI - Unidade II
# 18.05.2026 20h21
# Leitura e gravacao de arquivos csv, json, xml, parquet

# Importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import os

data = {
    'Categoria': ['Eletronicos', 'Roupas', 'Alimentos', 'Livros'],
    'Vendas': [1500, 800, 1200, 450]
}

df_original = pd.DataFrame(data)

# Gravando os arquivos
df_original.to_csv(path_or_buf = 'dados_venda.csv', index = False)
df_original.to_json(path_or_buf = "dados_venda.json", orient = 'records')
df_original.to_xml(path_or_buffer = 'dados_venda.xml', index = False)
df_original.to_parquet(path = 'dados_venda.parquet', index = False)

# Lendo os arquivos - simulacao de ingestao
df_csv = pd.read_csv('dados_venda.csv')
df_json = pd.read_json('dados_venda.json')
df_xml = pd.read_xml('dados_venda.xml')
df_parquet = pd.read_parquet('dados_venda.parquet')

# Interface Visual
fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (10,8))
fig.suptitle(t='Dados Recuperados de Diferentes Formatos', fontsize = 16)

# Plotando os graficos
formatos = [ 
    (df_csv, 'CSV', 'skyblue'),
    (df_json, 'JSON', 'salmon'),
    (df_xml, 'XML', 'lightgreen'),
    (df_parquet, 'Parquet', 'gold'),
]

for i, (df, titulo, cor) in enumerate(formatos):
    ax = axes[i//2, i%2]
    ax.bar(df['Categoria'], df['Vendas'], color = cor)
    ax.set_title(f'Origem: {titulo}.')
    ax.set_ylabel('Vendas')

plt.tight_layout(rect = [0, 0.03, 1, 0.95])
plt.show()