import streamlit as st
from PIL import Image

# Configurar la página
st.set_page_config(page_title="Registro Medtronic", page_icon="🩺", layout="centered")

# Layout con columnas para alinear el logo más a la derecha
col1, col2, col3 = st.columns([0.5, 1.5, 1])

with col3:
    try:
        logo = Image.open("logo_medtronic.png")
        st.image(logo, width=150)  # Puedes ajustar el tamaño si lo deseas
    except Exception as e:
        st.error(f"No se pudo cargar el logo: {e}")

# Contenido principal centrado
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Selector de tipo
tipo = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón continuar
if st.button("Continuar", use_container_width=True):
    st.session_state.tipo_operacion = tipo
    st.success(f"Iniciaste el proceso de **{tipo}**")








