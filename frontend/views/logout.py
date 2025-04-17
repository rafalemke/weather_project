import streamlit as st

def show_logout():
    st.title("🔒 Sair")
    st.warning("Tem certeza de que deseja sair?")

    if st.button("Sim"):
        for key in ["authenticated", "user_role", "df", "page", "last_page"]:
            st.session_state.pop(key, None)
        st.rerun()
