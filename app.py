import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Registro Medtronic", page_icon="🩺", layout="centered")

# Crear columnas para colocar el logo más a la izquierda (columna 2 de 3)
col1, col2, col3 = st.columns([1, 2, 2])  # col2 tiene más espacio (el logo va aquí)

with col2:
    try:
        logo = Image.open("logo_medtronic.png")
        st.image(logo, width=120)
    except Exception as e:
        st.error(f"No se pudo cargar el logo: {e}")

# Línea divisoria opcional
st.markdown("---")

# Título centrado
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Selector horizontal
tipo = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón continuar
if st.button("Continuar", use_container_width=True):
    st.session_state.tipo_operacion = tipo
    st.success(f"Iniciaste el proceso de **{tipo}**")









