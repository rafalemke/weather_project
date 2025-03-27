import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services import authenticate_user  # Agora o import funcionará


# Configuração da página
st.set_page_config(page_title="Dashboard", layout="wide")

# Tela de login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        user = authenticate_user(username, password)  # Autentica no banco de dados
        if user:
            st.session_state.authenticated = True
            st.session_state.user_role = user["role"]
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
else:
    # Menu lateral
    with st.sidebar:
        st.title("Menu")
        menu_option = st.radio(
            "Navegação",
            options=["Página Inicial", "Relatórios", "Configurações", "Sair"]
        )

    # Conteúdo principal
    if menu_option == "Página Inicial":
        st.title("Bem-vindo ao Dashboard")
        st.write("Esta é a página inicial.")

    elif menu_option == "Relatórios":
        st.title("Relatórios")
        st.write("Aqui estão os relatórios.")

    elif menu_option == "Configurações":
        if st.session_state.user_role == "admin":
            st.title("Configurações")
            st.write("Aqui você pode ajustar as configurações.")

            # Formulário para criar um novo usuário
            st.subheader("Criar Novo Usuário")
            new_username = st.text_input("Nome de Usuário")
            new_password = st.text_input("Senha", type="password")
            new_role = st.selectbox("Papel do Usuário", options=["user", "admin"])

            if st.button("Criar Usuário"):
                if new_username and new_password:
                    from backend.services import insert_user  # Importa a função para inserir usuários
                    try:
                        insert_user(new_username, new_password, new_role)
                        st.success(f"Usuário '{new_username}' criado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao criar usuário: {e}")
                else:
                    st.error("Por favor, preencha todos os campos.")
        else:
            st.error("Você não tem permissão para acessar esta página.")
            
    elif menu_option == "Sair":
        st.title("Sair")
        st.warning("Tem certeza de que deseja sair?")
        
        # Botões de confirmação
        confirm_logout = st.button("Sim")
        cancel_logout = st.button("Cancelar")

        if confirm_logout:
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.rerun()
        elif cancel_logout:
            st.experimentalrerun()  # Redireciona para evitar ações indesejadas