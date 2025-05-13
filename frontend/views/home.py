import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from backend.config import API_HOST, API_PORT
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import utils.visualizations as vis

# ========== Funções Auxiliares ==========

def fetch_api_data(url: str) -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        st.info("Verifique se o servidor da API está rodando e acessível.")
        return {}

def format_datetime(dt: str, fmt: str = "%d/%m/%Y %H:%M") -> str:
    if not dt:
        return "--"
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S").strftime(fmt)

def metric_card(title, value, unit, max_val, min_val, max_date, min_date, gradient, icon):
    st.markdown(f"""
        <div style="
            background: {gradient};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            color: white;
        ">
            <h2>{icon} {title}</h2>
            <h1 style="font-size: 2.5rem;">{value:.1f} {unit}</h1>
            <hr>
            <p>⬆️ Máx: {max_val:.1f} {unit}<br>📅 {max_date}</p>
            <p>⬇️ Mín: {min_val:.1f} {unit}<br>📅 {min_date}</p>
        </div>
    """, unsafe_allow_html=True)

def render_filter_options():
    variable_labels = {"temperature": "Temperatura", "pressure": "Pressão", "humidity": "Umidade"}
    days_labels = {1: "24 horas", 7: "7 dias", 30: "30 dias"}
    col_day, col_variable = st.columns(2)

    with col_day:
        selected_days = st.selectbox(
            "Selecione o período:",
            options=[1, 7, 30],
            format_func=lambda x: days_labels[x],
            index=[1, 7, 30].index(st.session_state.get("days", 1))
        )
        if selected_days != st.session_state.get("days", 1):
            st.session_state["days"] = selected_days
            st.rerun()

    with col_variable:
        selected_var = st.selectbox(
            "Selecione a variável:",
            options=list(variable_labels.keys()),
            format_func=lambda x: variable_labels[x],
            index=list(variable_labels.keys()).index(st.session_state.get("variable", "temperature"))
        )
        if selected_var != st.session_state.get("variable", "temperature"):
            st.session_state["variable"] = selected_var
            st.rerun()

# ========== Página Principal ==========

def show_home():
    st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")
    
    # Cabeçalho com relógio
    st.markdown("""
    <div style="text-align: center; padding-top: 10px;">
        <h1 style="margin-bottom: 0;">🌦️ Monitoramento Climático - Sítio Itacarnijó</h1>
        <div id="clock" style="
            display: inline-block;
            margin-top: 8px;
            background: linear-gradient(135deg, #1f1c2c, #928DAB);
            color: #ffffff;
            padding: 8px 20px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: 600;
            font-family: 'Courier New', monospace;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        ">🕒 --:--:--</div>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
        <script>
            function updateClock() {
                const clockEl = window.parent.document.getElementById("clock");
                if (clockEl) {
                    const now = new Date();
                    const time = now.toLocaleTimeString();
                    clockEl.innerHTML = "🕒 " + time;
                }
            }
            setInterval(updateClock, 1000);
            updateClock();
        </script>
    """, height=0, width=0)

    # Chamada da API
    API_URL = f"http://{API_HOST}:{API_PORT}/data?limit=3000"
    EXTREMOS_URL = f"http://{API_HOST}:{API_PORT}/extremos"

    data_json = fetch_api_data(API_URL)
    extremos = fetch_api_data(EXTREMOS_URL)

    if not data_json or "data" not in data_json:
        st.warning("Nenhum dado disponível no momento.")
        return

    data = data_json["data"]
    df = pd.DataFrame(data)
    last_reading = data[0]

    # Datas formatadas
    dates = extremos.get("dates", {})
    last_update = format_datetime(last_reading["date"], "%d/%m/%Y %H:%M:%S")
    temp_max_date = format_datetime(dates.get("temp_max"))
    temp_min_date = format_datetime(dates.get("temp_min"))
    press_max_date = format_datetime(dates.get("press_max"))
    press_min_date = format_datetime(dates.get("press_min"))
    hum_max_date = format_datetime(dates.get("hum_max"))
    hum_min_date = format_datetime(dates.get("hum_min"))

    # Cartões principais
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Temperatura", last_reading["temperature"], "°C",
                    extremos["max_temp"], extremos["min_temp"],
                    temp_max_date, temp_min_date,
                    "linear-gradient(135deg, #2980b9, #3498db)", "🌡️")
    with col2:
        metric_card("Pressão", last_reading["pressure"], "hPa",
                    extremos["max_pressure"], extremos["min_pressure"],
                    press_max_date, press_min_date,
                    "linear-gradient(135deg, #ff9966, #e67e22)", "🌬️")
    with col3:
        metric_card("Umidade", last_reading["humidity"], "%",
                    extremos["max_humidity"], extremos["min_humidity"],
                    hum_max_date, hum_min_date,
                    "linear-gradient(135deg, #56ab2f, #27ae60)", "💧")

    st.markdown(f"<br><p style='text-align: center; font-size: 1.2rem;'>Última atualização: {last_update}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Seção de análise histórica
    st.markdown("<div style='text-align: center;'><h1>📊 Análise Histórica</h1></div>", unsafe_allow_html=True)

    # Estado inicial
    st.session_state["days"] = st.session_state.get("days", 1)
    st.session_state["variable"] = st.session_state.get("variable", "temperature")

    render_filter_options()

    # Gráfico histórico
    st.pyplot(vis.plot_historic_data(
        df,
        variable=st.session_state["variable"],
        days=st.session_state["days"]
    ))

    st.markdown("---")
    st.subheader("ℹ️ Sobre os Dados")
    st.markdown("""
        Os dados são coletados em tempo real através de sensores conectados à uma API.  
        **Fonte dos dados:** Estação Meteorológica IoT ESP32 - Sensor BME280.  
        **Localização:** Município de Moreno/PE  
        **Frequência de atualização:** A cada 15 minutos  
    """)

    if st.button("🔄 Atualizar Dados"):
        st.rerun()
