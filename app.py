import streamlit as st
from PIL import Image

# Cargar el logo
logo = Image.open("logo_medtronic.png")

# Mostrar el logo centrado
st.image(logo, use_column_width=True)

# Título principal
st.markdown("<h1 style='text-align: center; color: #0A4D8C;'>Registro de Equipos</h1>", unsafe_allow_html=True)

# Espacio
st.markdown("###")

# Botones de navegación
col1, col2 = st.columns(2)

with col1:
    if st.button("🛠 Ingreso de equipo"):
        st.session_state["modo"] = "ingreso"

with col2:
    if st.button("📦 Salida de equipo"):
        st.session_state["modo"] = "salida"

# Navegación condicional
if "modo" in st.session_state:
    if st.session_state["modo"] == "ingreso":
        st.success("Has seleccionado: Ingreso de equipo ✅")
        # Aquí va el formulario de ingreso
    elif st.session_state["modo"] == "salida":
        st.info("Has seleccionado: Salida de equipo ✅")
        # Aquí va el formulario de salida





