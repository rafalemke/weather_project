import streamlit as st
import requests
from datetime import datetime
from backend.config import API_HOST, API_PORT
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

def show_home():
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

    API_URL = f"http://{API_HOST}:{API_PORT}/data?limit=1"
    EXTREMOS_URL = f"http://{API_HOST}:{API_PORT}/extremos"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()["data"]

        extremos_response = requests.get(EXTREMOS_URL)
        extremos_response.raise_for_status()
        extremos = extremos_response.json()

        if data:
            last_reading = data[0]
            last_update = datetime.strptime(last_reading["date"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
            temp_max_date = datetime.strptime(extremos["dates"]["temp_max"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")
            temp_min_date = datetime.strptime(extremos["dates"]["temp_min"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")
            press_max_date = datetime.strptime(extremos["dates"]["press_max"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")
            press_min_date = datetime.strptime(extremos["dates"]["press_min"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")
            hum_max_date = datetime.strptime(extremos["dates"]["hum_max"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")
            hum_min_date = datetime.strptime(extremos["dates"]["hum_min"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")


            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #ff9966, #ff5e62);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        text-align: center;
                        color: white;
                    ">
                        <h2>🌡️ Temperatura</h2>
                        <h1 style="font-size: 2.5rem;">{last_reading["temperature"]:.1f} °C</h1>                        
                        <p>⬆️ Máx: {extremos["max_temp"]:.1f} °C<br>📅 {temp_max_date}</p>
                        <p>⬇️ Mín: {extremos["min_temp"]:.1f} °C<br>📅 {temp_min_date}</p>   

                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #4b6cb7, #182848);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        text-align: center;
                        color: white;
                    ">
                        <h2>🌬️ Pressão</h2>
                        <h1 style="font-size: 2.5rem;">{last_reading["pressure"]:.1f} hPa</h1>
                        <p>⬆️ Máx: {extremos["max_pressure"]:.1f} hPa<br>📅 {press_max_date}</p>
                        <p>⬇️ Mín: {extremos["min_pressure"]:.1f} hPa<br>📅 {press_min_date}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #56ab2f, #a8e063);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        text-align: center;
                        color: white;
                    ">
                        <h2>💧 Umidade</h2>
                        <h1 style="font-size: 2.5rem;">{last_reading["humidity"]:.1f} %</h1>
                        <p>⬆️ Máx: {extremos["max_humidity"]:.1f} %<br>📅 {hum_max_date}</p>
                        <p>⬇️ Mín: {extremos["min_humidity"]:.1f} %<br>📅 {hum_min_date}</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <br>
            <p style="text-align: center; font-size: 1.2rem;">
                        Última atualização: {last_update}
            </p>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("ℹ️ Sobre os Dados")
            st.markdown("""
            Os dados são coletados em tempo real através de sensores conectados à uma API.  
            **Fonte dos dados:** Estação Meteorológica IoT ESP32 - Sensor BME280.  
            **Localização:** Município de Moreno/PE  
            **Frequência de atualização:** A cada 5 minutos  
            """)

        else:
            st.warning("Nenhum dado disponível no momento. Verifique a conexão com os sensores.")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        st.info("Verifique se o servidor da API está rodando e acessível.")

    if st.button("🔄 Atualizar Dados"):
        st.rerun()
