# Importando as bibliotecas
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Configurando a pagina do StreamLit
st.set_page_config(page_title = "Lumina Energy Analitycs", layout = "wide", page_icon="⚡")

# Carregando o arquivo gerado na Camada Ouro
ARQUIVO_OURO = "data_lakehouse/ouro/fatoRecarga.parquet"

# Informacoes de Titulo
st.title("Lumina Energy - Dashboard de Operacoes e Sentimento")
st.markdown("Análise cruzando Iot, Faturamento e Sentimento do Mercado.")
st.write("----")

# Verificando a existencia do arquivo e carregando ele
if os.path.exists(ARQUIVO_OURO):
    df_fato = pd.read_parquet(ARQUIVO_OURO)
    df_fato["DataHora"] = pd.to_datetime(df_fato["DataHora"])

    # Definindo os indicadores de performance
    ind1, ind2, ind3, ind4 = st.columns(4)
    with ind1: 
        st.metric("Total de Recargas(IoT): ", f"{len(df_fato)}".replace(",", "."))
    with ind2:
        st.metric("Potencia Total Consumida: ", f"{df_fato['DemandaPotencia_kW'].sum():.2f} kW.")
    with ind3:
        st.metric("Faturamento Real Correlacionado", f"R$ {df_fato['ValorPagamento'].sum():.2f}.")
    with ind4:
        st.metric("Media do Sentimento Publico: ", f"{df_fato['ScoreSentimento'].mean():.2f}.")
    st.write("---")

    # Agrupando por hora o grafico de linhas temporais
    df_temporal = df_fato.groupby("DataHora").agg({
        "DemandaPotencia_kW": "sum",
        "ScoreSentimento": "mean"
        }).reset_index()

    # Grafico de Correlação: Sentimento do Mercado vs Demanda de Energia
    st.subheader("Correlação: Demanda VS Sentimento")

    # Criando o gráfico
    fig = px.line(df_temporal, x = "DataHora", y = "DemandaPotencia_kW", 
                  title = "Evolucao da Demanda de Potencia nos Eletropostos",
                  labels = {"DemandaPotencia_kW": "Potencia (kW)", "DataHora": "Tempo (Horas)"})
    
    fig.update_traces(line_color = "#FF4B4B", line_width = 3)
    st.plotly_chart(fig, use_container_width = True)

    # Grafico de Comportamento do Sentimento
    fig_sent = px.bar(df_temporal, x = "DataHora", y = "ScoreSentimento",
                      title = "Score de Sentimento do Mercado",
                      labels = {"ScoreSentimento": "(-1 a +1)", "DataHora": "Tempo (Horas)"},
                      color = "ScoreSentimento", color_continuous_scale = px.colors.sequential.Blues)
    st.plotly_chart(fig_sent, use_container_width = True)

    # Visualizando os dados da TAbela Fato
    st.subheader("Visualizacao da Camada Ouro")
    st.dataframe(df_fato.head(5000), use_container_width = True)

else:
    st.error(f"❌ O arquivo da camada Ouro não foi encontrado em: {ARQUIVO_OURO}. Certifique-se de executar o pipeline primeiro.")
