import streamlit as st
import psutil, os, stat, signal, time

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

st.header("Processos")

with st.form("excluirProcesso"):
    pid = st.number_input("Insira o PID do processo para exclui-lo", value=0)

    excluir = st.form_submit_button("Excluir")

    if(excluir):
        # processo = psutil.Process(pid)
        # os.chmod(processo.exe(), stat.S_IRWXO)
        os.kill(pid, signal.SIGKILL)

processos = psutil.process_iter()

tabela = """
    <table>
        <thead>
            <th>PID</th>
            <th>Nome</th>
            <th>Usuário</th>
            <th>%CPU</th>
            <th>%MEM</th>
            <th></th>
        </thead>
        <tbody>
"""

for processo in processos:
    try:
        tabela += f"""
            <tr>
                <td>{processo.pid}</td>
                <td>{processo.name()}</td>
                <td>{processo.username()}</td>
                <td>{round(processo.cpu_percent(), 2)}</td>
                <td>{round(processo.memory_percent(), 2)}</td>
            </tr>
        """
    except psutil.NoSuchProcess:
        pass

tabela += """
        </tbody>
    </table>
"""

st.html(tabela)

time.sleep(1)
st.rerun()