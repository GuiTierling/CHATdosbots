import streamlit as st
from huggingface_hub import InferenceClient

client = InferenceClient(token=st.secrets["HF_TOKEN"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat_completion(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=st.session_state.messages,
        max_tokens=500,
    )
    
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)