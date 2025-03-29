import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.security import authenticate_user 

# Configuração da página
st.set_page_config(page_title="Dashboard", layout="wide")

# Estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# Tela de login
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user_role = user["role"]
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
else:
    # Exibe a interface do dashboard apenas após autenticação
    st.sidebar.title("Menu")
    menu_options = ["Página Inicial", "Relatórios"]  # Opções padrão do menu
    # Adiciona "Configurações" ao menu se o usuário for admin
    if st.session_state.user_role == "admin":
        menu_options.append("Configurações")  # Adiciona "Configurações" se o usuário for admin

    menu_options.append("Sair")  # Adiciona "Sair" ao menu
    
    # Cria o menu lateral
    menu_option = st.sidebar.radio("Navegação", menu_options)

    

    # Importa dinamicamente a página selecionada
    if menu_option == "Página Inicial":
        from views.home import show_home
        show_home()

    elif menu_option == "Relatórios":
        from views.reports import show_reports
        show_reports()

    elif menu_option == "Configurações":
        from views.settings import show_settings
        show_settings()

    elif menu_option == "Sair":
        from views.logout import show_logout
        show_logout()