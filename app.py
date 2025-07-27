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
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.image(logo, width=200)
except Exception as e:
    st.warning(f"No se pudo cargar el logo: {e}")

st.markdown("## ¿Qué deseas registrar?")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    tipo_operacion = st.radio("Selecciona una opción:", ["Ingreso", "Salida"], horizontal=True)

if "equipos" not in st.session_state:
    st.session_state.equipos = []

if st.button("Agregar equipo"):
    st.session_state.equipos.append({"nombre": "", "serial": ""})

for i, equipo in enumerate(st.session_state.equipos):
    st.write(f"### Equipo {i+1}")
    cols = st.columns([4, 4, 1])
    equipo["nombre"] = cols[0].text_input(f"Nombre del equipo {i+1}", value=equipo["nombre"], key=f"nombre_{i}")
    equipo["serial"] = cols[1].text_input(f"Serial del equipo {i+1}", value=equipo["serial"], key=f"serial_{i}")
    if cols[2].button("Eliminar", key=f"eliminar_{i}"):
        st.session_state.equipos.pop(i)
        st.experimental_rerun()

if st.button("Continuar"):
    st.session_state["tipo_operacion"] = tipo_operacion
    st.success(f"Seleccionaste: {tipo_operacion}")
    st.write("Equipos registrados:")
    for equipo in st.session_state.equipos:
        st.write(f"- {equipo['nombre']} (Serial: {equipo['serial']})")















