from google import genai
import streamlit as st

st.title(
    "🤖 Tutor de Programación con IA del IES Pío Baroja Departamento de Informática"
)

# 1. Configurar el cliente de la API
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Definir las instrucciones de sistema (rol socrático)
system_prompt = """
Actúa estrictamente como un profesor socrático de programación. 
NUNCA des código fuente directo ni soluciones completas al usuario. 
Guía su razonamiento lógico mediante preguntas orientadoras y analogías cotidianas.
"""

# 3. Inicializar el historial de mensajes en la sesión de Streamlit si no existe
if "messages" not in st.session_state:
  st.session_state.messages = []

# 4. Mostrar los mensajes anteriores guardados en la sesión al recargar la página
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 5. Capturar la nueva entrada del usuario
if user_input := st.chat_input("Escribe tu duda o pega tu código aquí..."):
  # Añadir y mostrar el mensaje del usuario inmediatamente
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generar la respuesta del asistente usando el modelo con system_instruction
  with st.chat_message("assistant"):
    with st.spinner("Pensando una buena pregunta..."):
      try:
        # Preparamos el historial para enviarlo al modelo en cada turno
        contents = []
        for m in st.session_state.messages:
          contents.append(f"{m['role']}: {m['content']}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={"system_instruction": system_prompt},
        )

        bot_reply = response.text
        st.markdown(bot_reply)

        # Guardar la respuesta del asistente en el historial
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )
      except Exception as e:
        st.error(f"Ocurrió un error al conectar con la IA: {e}")