import streamlit as st
import psutil
import time

if("usoMemoria" not in st.session_state):
    st.session_state.usoMemoria = []
if("usoCPU" not in st.session_state):
    st.session_state.usoCPU = []

def usoMemoria():
    valorMemoria = psutil.virtual_memory().percent
    st.session_state.usoMemoria.append(valorMemoria)

    st.session_state.usoMemoria = st.session_state.usoMemoria[-60:]

def usoCPU():
    valorCPU = psutil.cpu_percent()
    st.session_state.usoCPU.append(valorCPU)

    st.session_state.usoCPU = st.session_state.usoCPU[-60:]

st.title("Gerenciador de Processos e Permissões")

usoMemoria()
usoCPU()

st.header("Uso de Memória (%)")
st.line_chart(st.session_state.usoMemoria)

st.header("Uso da CPU (%)")
st.line_chart(st.session_state.usoCPU)

time.sleep(1)

st.rerun()