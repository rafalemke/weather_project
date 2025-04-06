import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go
from backend.config import API_HOST, API_PORT
from datetime import datetime, timedelta

# URL da API
API_URL = f"http://{API_HOST}:{API_PORT}/data"

def show_reports():
    st.title("Relatórios Meteorológicos 🌦️")
    st.markdown("---")
    st.subheader("📈 Gerar Gráfico")

    # Inicializar variáveis de estado
    if 'export_format' not in st.session_state:
        st.session_state.export_format = "CSV"
    if 'df' not in st.session_state:
        st.session_state.df = None

    # Seleção de intervalo de datas
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data inicial", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("Data final", datetime.now())

    # Botão para buscar dados
    if st.button("Buscar dados"):
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()["data"]

            if not data:
                st.warning("Nenhum dado encontrado para o período selecionado.")
                return

            # 2. Criar DataFrame e processar os dados
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()
            df = df.rolling(window=1, min_periods=1).mean()
            st.session_state.df = df.reset_index()
            

            # 3. Aplicar suavização
            df["temperature"] = df["temperature"].rolling(window=1, min_periods=1).mean()
            df["pressure"] = df["pressure"].rolling(window=1, min_periods=1).mean()
            df["humidity"] = df["humidity"].rolling(window=1, min_periods=1).mean()

            

            # 4. Criar a figura
            fig = go.Figure()

            # Adicionando a linha de temperatura (sempre visível)
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["temperature"],
                mode='lines',
                name="Temperatura",
                yaxis="y1",
                
                line=dict(shape="spline", smoothing=1)
            ))

            # Adicionando a linha de pressão (inicialmente visível)
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["pressure"],
                mode='lines',
                name="Pressão",
                yaxis="y2",
                visible=True,
                line=dict(shape="spline", smoothing=1)
            ))

            # Adicionando a linha de umidade (inicialmente oculta)
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["humidity"],
                mode='lines',
                name="Umidade",
                yaxis="y2",
                visible=False,
                line=dict(shape="spline", smoothing=1)
            ))

            # 5. Configuração do layout
            # 5. Configuração do layout (parte modificada)
            # 5. Configuração do layout (parte modificada)
            fig.update_layout(
                title={
                    "text": "Temperatura e Pressão/Humidade ao Longo do Tempo",
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                },
                xaxis=dict(title="Hora"),
                yaxis=dict(
                    title="Temperatura (°C)", 
                    side="left",
                    range=[df["temperature"].min() - 1, df["temperature"].max() + 1]  # Range para temperatura com margem de 1°C
                ),
                yaxis2=dict(
                    title="Pressão (hPa)", 
                    overlaying="y", 
                    side="right", 
                    showgrid=False,
                    range=[df["pressure"].min() - 5, df["pressure"].max() + 5]
                ),
                legend=dict(
                    x=0.9,
                    y=1.1,
                    xanchor="center",
                    yanchor="top",
                    orientation="h"
                ),
                template="plotly_dark",
                updatemenus=[{
                    "buttons": [
                        {
                            "label": "🌬️ Pressão",
                            "method": "update",
                            "args": [
                                {"visible": [True, True, False]},
                                {
                                    "yaxis2.title.text": "Pressão (hPa)",
                                    "yaxis2.range": [df["pressure"].min() - 5, df["pressure"].max() + 5]
                                }
                            ],
                            "args2": [{"transition": {"duration": 500}}]
                        },
                        {
                            "label": "💧 Umidade",
                            "method": "update",
                            "args": [
                                {"visible": [True, False, True]},
                                {
                                    "yaxis2.title.text": "Umidade (%)",
                                    "yaxis2.range": [df["humidity"].min() - 5, df["humidity"].max() + 5]
                                }
                            ],
                            "args2": [{"transition": {"duration": 500}}]
                        }
                    ],
                    "direction": "down",
                    "showactive": True,
                    "x": 0.12,
                    "y": 1.17,
                    "font": dict(color="black"),
                    "bgcolor": "#555555",
                    "bordercolor": "white",
                    "borderwidth": 1,
                    "active": 0,
                }]
            )

            # 6. Exibir o gráfico
            st.plotly_chart(fig, use_container_width=True)
          

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar dados da API: {e}")
    
    # Seção de exportação (só aparece se existirem dados)
    if st.session_state.df is not None:
        st.markdown("---")
        st.subheader("📤 Exportar Dados")

        if "filename_input" not in st.session_state:
            st.session_state.filename_input = f"dados_climaticos_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        with st.form("export_form"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.selectbox(
                    "Formato",
                    ["CSV", "JSON", "Excel"],
                    key="export_format_selectbox"
                )

            with col2:
                st.text_input(
                    "Nome do Arquivo",
                    key="filename_input",
                    placeholder="Ex: dados_meteorologicos"
                )

            submitted = st.form_submit_button("📁 Gerar Arquivo")

        if submitted:
            df_export = st.session_state.df
            export_format = st.session_state.export_format_selectbox
            filename = st.session_state.filename_input.strip()

            if not filename:
                st.warning("Por favor, insira um nome de arquivo válido.")
                return

            if export_format == "CSV":
                data = df_export.to_csv(index=False).encode("utf-8")
                mime = "text/csv"
                extension = "csv"
            elif export_format == "JSON":
                data = df_export.to_json(orient="records", indent=4).encode("utf-8")
                mime = "application/json"
                extension = "json"
            elif export_format == "Excel":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df_export.to_excel(writer, index=False)
                data = output.getvalue()
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                extension = "xlsx"

            st.success("✅ Arquivo gerado com sucesso!")

            st.download_button(
                label=f"⬇️ Baixar {export_format}",
                data=data,
                file_name=f"{filename}.{extension}",
                mime=mime,
                use_container_width=True,
                key=f"download_button_{datetime.now().timestamp()}"
            )