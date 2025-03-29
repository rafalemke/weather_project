import streamlit as st
from backend.services import insert_user

def show_settings():
    if st.session_state.user_role == "admin":
        st.title("⚙️ Configurações")

        # Criar usuário
        st.subheader("Criar Novo Usuário")
        new_username = st.text_input("Nome de Usuário")
        new_password = st.text_input("Senha", type="password")
        new_role = st.selectbox("Papel do Usuário", ["user", "admin"])

        if st.button("Criar Usuário"):
            if new_username and new_password:
                try:
                    insert_user(new_username, new_password, new_role)
                    st.success(f"Usuário '{new_username}' criado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao criar usuário: {e}")
            else:
                st.error("Por favor, preencha todos os campos.")
    else:
        st.error("Você não tem permissão para acessar esta página.")
