import streamlit as st
from PIL import Image

# Configurar la página
st.set_page_config(page_title="Registro Medtronic", page_icon="🩺", layout="centered")

# Centrar todo con columnas vacías
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Mostrar logo centrado
    try:
        logo = Image.open("logo_medtronic.png")
        st.image(logo, width=200)
    except Exception as e:
        st.error(f"No se pudo cargar el logo: {e}")

    # Título principal
    st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)
    
    # Botones
    tipo = st.radio("", ["Ingreso", "Salida"], horizontal=True)

    if st.button("Continuar", use_container_width=True):
        st.session_state.tipo_operacion = tipo
        st.success(f"Iniciaste el proceso de **{tipo}**")

        # Aquí puedes continuar mostrando los campos del formulario, etc.







