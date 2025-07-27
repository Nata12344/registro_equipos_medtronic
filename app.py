import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Registro de equipo - Medtronic",
    layout="centered",
    page_icon="🔧"
)

# Cargar y mostrar logo pequeño
try:
    logo = Image.open("logo_medtronic.png")
    st.image(logo.resize((200, 200)), use_column_width=False)
except Exception as e:
    st.error(f"No se pudo cargar el logo: {e}")

# Título centrado
st.markdown("<h3 style='text-align: center; color: black;'>¿Qué deseas registrar?</h3>", unsafe_allow_html=True)

# Botones centrados
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    ingreso = st.button("🛠 Ingreso", use_container_width=True)
    salida = st.button("📦 Salida", use_container_width=True)

# Guardar selección y mostrar mensaje o cambiar de vista
if ingreso:
    st.session_state["modo"] = "Ingreso"
if salida:
    st.session_state["modo"] = "Salida"

if "modo" in st.session_state:
    st.markdown(f"### Has seleccionado: {st.session_state['modo']} de equipo ✅")

    # Aquí podemos insertar el formulario de ingreso o salida
    # Por ahora mostramos un mensaje
    if st.session_state["modo"] == "Ingreso":
        st.info("Aquí irá el formulario de ingreso 🛠")
    elif st.session_state["modo"] == "Salida":
        st.info("Aquí irá el formulario de salida 📦")






