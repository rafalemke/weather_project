import streamlit as st

def show_logout():
    st.title("🔒 Sair")
    st.warning("Tem certeza de que deseja sair?")

    if st.button("Sim, sair"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()
