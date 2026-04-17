import streamlit as st
from main import agent_executor 
st.set_page_config(page_title="IA Analyste Financier", layout="wide")

with st.sidebar:
    st.header("🛠 Outils Actifs")
    st.write("- 📊 SQL Database (Clients/Produits)")
    st.write("- 📈 yfinance (Bourse réelle)")
    st.write("- 🔍 Tavily (Recherche Web)")
    st.write("- 🐍 PythonREPL (Calculs)")
    
    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        agent_executor.memory.clear()
        st.rerun()

st.title("🤖 Assistant Financier Intelligent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez une question (ex: Infos Sophie Bernard...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'agent réfléchit..."):
            response = agent_executor.invoke({"input": prompt})
            full_response = response["output"]
            st.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})