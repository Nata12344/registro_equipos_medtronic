import streamlit as st
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import os

# Configuración inicial
st.set_page_config(page_title="Registro de Equipos Medtronic", layout="wide")

# Variables fijas
correos_ingenieros = {
    "Nicolle Riaño": "nicolle.n.riano@medtronic.com"
}

if "equipos" not in st.session_state:
    st.session_state.equipos = []

if "tipo_operacion" not in st.session_state:
    st.session_state.tipo_operacion = "Ingreso"

# Encabezado dinámico
titulo_encabezado = f"{st.session_state.tipo_operacion} - Registro de equipos"

# Mostrar encabezado con fondo azul
st.markdown(
    f"""
    <div style="background-color:#00338D; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Medtronic_logo.svg/2560px-Medtronic_logo.svg.png" alt="Medtronic Logo" style="height: 50px; margin-right: 20px;">
            <div style="color: white;">
                <h2 style="margin: 0;">{titulo_encabezado}</h2>
                <p style="margin: 0;">Información confidencial - Uso exclusivo de Medtronic</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Formulario
col1, col2 = st.columns(2)

with col1:
    st.session_state.tipo_operacion = st.selectbox("Tipo de movimiento", ["Ingreso", "Salida"])
    cliente = st.text_input("Cliente (Hospital o Medtronic)", key="cliente")
    ingeniero = st.selectbox("Ingeniero responsable", list(correos_ingenieros.keys()), key="ingeniero")
with col2:
    nombre_equipo = st.text_input("Nombre del equipo")
    serial_equipo = st.text_input("Número de serial")
    imagen_equipo = st.file_uploader("Adjuntar imagen", type=["jpg", "jpeg", "png"])

# Botón para agregar equipo
if st.button("Agregar equipo"):
    if nombre_equipo and serial_equipo and imagen_equipo:
        st.session_state.equipos.append({
            "nombre": nombre_equipo,
            "serial": serial_equipo,
            "imagen": imagen_equipo.read()
        })
        st.success("Equipo agregado correctamente.")
    else:
        st.warning("Por favor completa todos los campos del equipo.")

# Mostrar lista de equipos agregados
if st.session_state.equipos:
    st.subheader("Equipos agregados:")
    for idx, eq in enumerate(st.session_state.equipos):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"**Equipo:** {eq['nombre']}")
            st.markdown(f"**Serial:** {eq['serial']}")
        with col2:
            st.image(eq['imagen'], width=150)
        with col3:
            if st.button("Eliminar", key=f"eliminar_{idx}"):
                st.session_state.equipos.pop(idx)
                st.success("Equipo eliminado.")
                st.experimental_rerun()

# Envío de correo
if st.session_state.equipos and st.button("Enviar correo"):
    try:
        remitente = "tucorreo@dominio.com"  # Cambia esto
        destinatario = correos_ingenieros.get(ingeniero)
        asunto = f"{st.session_state.tipo_operacion} de equipos - {cliente}"

        # Construir cuerpo del correo en HTML
        html = f"""<html><body>
        <p><b>{'Ingreso a Servicio Técnico' if st.session_state.tipo_operacion == 'Ingreso' else 'Salida de Servicio Técnico'}</b></p>
        <p><b>Cliente:</b> {cliente}<br>
        <b>Ingeniero:</b> {ingeniero}</p>
        <ul>"""

        for eq in st.session_state.equipos:
            html += f"<li><b>Equipo:</b> {eq['nombre']}<br><b>Serial:</b> {eq['serial']}</li>"
        html += "</ul></body></html>"

        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(html, "html"))

        # Adjuntar imágenes
        for idx, eq in enumerate(st.session_state.equipos):
            img = MIMEImage(eq["imagen"])
            img.add_header("Content-ID", f"<imagen{idx}>")
            img.add_header("Content-Disposition", "attachment", filename=f"{eq['nombre']}_{idx}.jpg")
            mensaje.attach(img)

        # Enviar correo
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login("tucorreo@dominio.com", "tu_contraseña")  # Cambia esto
            servidor.send_message(mensaje)

        st.success("Correo enviado correctamente.")
        st.session_state.equipos = []
    except Exception as e:
        st.error(f"Ocurrió un error al enviar el correo: {e}")




















