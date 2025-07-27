import streamlit as st
from PIL import Image

st.set_page_config(layout="centered", page_title="Registro de equipo - Medtronic")
st.markdown("""
    <style>
    .css-1v0mbdj, .css-1dp5vir, .stApp {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Diccionario de correos
correos_ingenieros = {
    "Nicolle Riaño": "nicolle.n.riano@medtronic.com"
}

# Logo
try:
    logo = Image.open("logo_medtronic.png")
    st.image(logo, width=200)
except Exception as e:
    st.warning(f"No se pudo cargar el logo: {e}")

st.markdown("## ¿Qué deseas registrar?")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    tipo_operacion = st.radio("Selecciona una opción:", ["Ingreso", "Salida"], horizontal=True)

if st.button("Continuar"):
    st.session_state["tipo_operacion"] = tipo_operacion
    st.success(f"Seleccionaste: {tipo_operacion}")
    # Aquí puedes continuar con el resto de la interfaz según la opción seleccionada












