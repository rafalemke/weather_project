import streamlit as st
import pandas as pd
from frontend.api_request import fetch_data_from_api
from data.datasets import temperature_chart


def show_home():
    st.title("📊 Dashboard Meteorológico")

    try:
        # Busca os dados da API
        df = pd.DataFrame(fetch_data_from_api())

        # Conversão de dados para tipo numérico
        df['temperature'] = pd.to_numeric(df['temperature'])
        df['pressure'] = pd.to_numeric(df['pressure'])
        df['humidity'] = pd.to_numeric(df['humidity'])

        # Seleção da variável para o gráfico
        selected_variable = st.radio("Escolha a variável para comparação:", ["pressure", "humidity"], index=0)

        # Criando o gráfico de temperatura e variável escolhida
        fig = temperature_chart(df, second_variable=selected_variable)

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
