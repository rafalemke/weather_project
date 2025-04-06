import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.security import authenticate_user 

# Configuração da página
st.set_page_config(page_title="Dashboard Climático - Sítio Itacarnijo", layout="wide")

# Estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.name = None
    st.session_state.login_clicked = False
    st.session_state.pop("df", None)

# CSS personalizado para o botão de login
st.markdown("""
<style>
    .login-button {
        background: linear-gradient(135deg, #56ab2f, #a8e063);
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }
    .login-button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .header-anchor {
        display: none !important;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Exibe a página Home por padrão
if not st.session_state.authenticated:
    from views.home import show_home
    show_home()
    
    # Overlay de login
    with st.sidebar:
        st.title("🔒 Acesso Restrito")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        # Botão de login personalizado único
        if st.button("Acessar Sistema", key="login_btn"):
            st.session_state.login_clicked = True
            
        if st.session_state.login_clicked:
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_role = user["role"]
                st.session_state.name = user["name"]
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas")
                st.session_state.login_clicked = False
else:
    # Menu lateral para usuários autenticados
    with st.sidebar:
        st.title(f"👋 Olá, {st.session_state.name.capitalize()}")
        
        # Opções do menu baseadas no perfil
        menu_options = ["Página Inicial", "Relatórios"]
        if st.session_state.user_role == "admin":
            menu_options.append("Configurações")
        
        menu_options.append("Sair")
        
        menu_option = st.radio("Navegação", menu_options)

    # Carrega a página selecionada
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