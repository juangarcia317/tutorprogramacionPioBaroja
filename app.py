from google import genai
import streamlit as st

st.title("🤖 Tutor de Programación con IA del IES Pío Baroja Departamento de Informática")

# 1. Configurar la clave y el cliente
# Asegúrate de que tienes configurado el secreto GEMINI_API_KEY en Streamlit Cloud
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Definir las instrucciones de sistema (rol socrático)
system_prompt = """
Actúa estrictamente como un profesor socrático de programación. 
NUNCA des código fuente directo ni soluciones completas al usuario. 
Guía su razonamiento lógico mediante preguntas orientadoras y analogías cotidianas.
"""

# 3. Inicializar la sesión de chat si no existe
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_prompt},
    )

# 4. Mostrar el historial previo del chat en la interfaz
for message in st.session_state.chat.get_history():
    # Ajustar el rol según la estructura del SDK
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        # Validar que los partes del mensaje existan antes de renderizar
        if message.parts:
            st.markdown(message.parts[0].text)

# 5. Capturar la entrada del usuario de manera segura
if user_input := st.chat_input("Escribe tu duda o pega tu código aquí..."):
    # Todo esto va indentado dentro del 'if'
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando una buena pregunta..."):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)