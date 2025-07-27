import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Registro Medtronic", page_icon="🩺", layout="centered")

# Crear espacio superior para el logo en la parte derecha
col1, col2, col3 = st.columns([2, 1, 1])  # col3 tiene más peso hacia la derecha

with col3:
    try:
        logo = Image.open("logo_medtronic.png")
        st.image(logo, width=120)  # Ajusta el tamaño si es necesario
    except Exception as e:
        st.error(f"No se pudo cargar el logo: {e}")

# Espaciado opcional
st.markdown("---")

# Texto centrado
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Selector horizontal
tipo = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón continuar
if st.button("Continuar", use_container_width=True):
    st.session_state.tipo_operacion = tipo
    st.success(f"Iniciaste el proceso de **{tipo}**")








