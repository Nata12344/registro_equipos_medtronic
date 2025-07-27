import streamlit as st
import base64

# Cargar la imagen del logo desde el archivo subido
with open("logo_medtronic.png", "rb") as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode()

# Mostrar logo alineado a la izquierda (ajustable)
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{image_base64}" width="160" style="margin-right: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Línea divisoria
st.markdown("---")

# Título centrado
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Opciones Ingreso / Salida
opcion = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón para continuar
if st.button("Continuar"):
    st.success(f"Seleccionaste: {opcion}")











