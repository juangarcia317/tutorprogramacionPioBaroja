from google import genai
import streamlit as st

st.title("🤖 Tutor de Programación con IA del IES Pío Baroja Departamento de Informática")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

system_prompt = """Actúa estrictamente como un profesor socrático de programación. NUNCA des código fuente directo ni soluciones completas. Guía el razonamiento mediante preguntas orientadoras."""

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_prompt}
    )

for message in st.session_state.chat.get_history():
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if user_input := st.chat_input("Escribe tu duda o pega tu código aquí..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(user_input)
        st.markdown(response.text)