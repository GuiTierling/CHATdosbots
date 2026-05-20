import streamlit as st
from huggingface_hub import InferenceClient

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatBot IA",
    page_icon="🤖",
    layout="centered",
)

# ── Estilo CSS ──────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .stChatMessage { border-radius: 15px; padding: 10px; }
        .stChatInputContainer { border-top: 2px solid #6c63ff; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Cliente HuggingFace ─────────────────────────────────────────────────────
client = InferenceClient(token=st.secrets["HF_TOKEN"])

# ── Inicializa sessão ───────────────────────────────────────────────────────
if "conversas" not in st.session_state:
    st.session_state.conversas = []  # lista de conversas
if "conversa_atual" not in st.session_state:
    st.session_state.conversa_atual = []  # mensagens da conversa aberta

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 ChatBot IA")
    st.divider()

    # Botão nova conversa
    if st.button("➕ Nova conversa"):
        if st.session_state.conversa_atual:
            st.session_state.conversas.append(st.session_state.conversa_atual.copy())
        st.session_state.conversa_atual = []
        st.rerun()

    st.markdown("### 🕘 Histórico")

    # Lista de conversas anteriores
    for i, conversa in enumerate(reversed(st.session_state.conversas)):
        # Pega a primeira mensagem como título
        titulo = conversa[0]["content"][:30] + "..." if conversa else f"Conversa {i+1}"
        if st.button(f"💬 {titulo}", key=f"conversa_{i}"):
            st.session_state.conversa_atual = conversa.copy()
            st.rerun()

    st.divider()
    if st.button("🗑️ Limpar histórico"):
        st.session_state.conversas = []
        st.session_state.conversa_atual = []
        st.rerun()

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align: center;'>🤖 ChatBot IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Desenvolvido por Guilherme Tierling, Samuel Nunes, Giovana Dutra e Ludmila França</p>", unsafe_allow_html=True)
st.divider()

# ── Mensagem de boas-vindas ─────────────────────────────────────────────────
if len(st.session_state.conversa_atual) == 0:
    st.markdown("<p style='text-align: center; color: gray;'>👋 Olá! Como posso te ajudar hoje?</p>", unsafe_allow_html=True)

# ── Exibe mensagens da conversa atual ──────────────────────────────────────
for msg in st.session_state.conversa_atual:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Input ────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("💬 Digite sua mensagem..."):
    st.session_state.conversa_atual.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=st.session_state.conversa_atual,
                max_tokens=500,
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.conversa_atual.append({"role": "assistant", "content": reply})