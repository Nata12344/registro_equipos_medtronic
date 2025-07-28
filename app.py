import streamlit as st
from PIL import Image

st.set_page_config(page_title="Test Sidebar", layout="centered")

# Sidebar de prueba
with st.sidebar:
    st.markdown("## Menú de Registro")
    st.button("Ingreso")
    st.button("Salida")
    st.markdown("Información confidencial - Medtronic")

st.markdown("### Bienvenido")
st.write("Este es un test para verificar que el menú lateral funcione.")




















