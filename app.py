import streamlit as st
from PIL import Image
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

# Configuración de página
st.set_page_config(page_title="Registro de Equipos", layout="centered")

# Cargar logo
logo_path = "fe208d28-cd21-4207-adb3-bb3e916d9641.png"
logo = Image.open(logo_path)

# --- ENCABEZADO ---
with st.container():
    st.markdown(
        """
        <div style='display: flex; align-items: center; background-color: #005DAA; padding: 10px; border-radius: 10px;'>
            <div style='flex: 0 0 auto; margin-right: 15px;'>
                <img src='data:image/png;base64,{}' width='80'>
            </div>
            <div style='flex: 1; text-align: center; color: white;'>
                <h4 style='margin-bottom: 5px;'>Información confidencial - Uso exclusivo de Medtronic</h4>
                <h2 style='margin-top: 0px;'>Ingreso o Salida – Registro de Equipos</h2>
            </div>
        </div>
        """.format(base64.b64encode(open(logo_path, "rb").read()).decode()),
        unsafe_allow_html=True
    )

# --- FORMULARIO ---
st.write("## Datos del Movimiento")

cliente = st.text_input("Cliente (ej: Hospital San Juan)")
ingeniero = st.text_input("Ingeniero responsable (ej: Nicolle Riaño)")
tipo_movimiento = st.radio("Tipo de movimiento", ["Ingreso", "Salida"])
comentarios = st.text_area("Comentarios adicionales")

# Equipos agregados dinámicamente
st.write("### Equipos registrados")
if "equipos" not in st.session_state:
    st.session_state.equipos = []

# Agregar nuevo equipo
with st.form("agregar_equipo"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del equipo", key="nombre_equipo")
    with col2:
        serial = st.text_input("Serial", key="serial_equipo")
    agregar = st.form_submit_button("Agregar equipo")
    if agregar and nombre and serial:
        st.session_state.equipos.append((nombre, serial))

# Mostrar lista de equipos
for i, (nombre, serial) in enumerate(st.session_state.equipos):
    st.markdown(f"**{i+1}. {nombre}** - Serial: `{serial}`")
    if st.button(f"Eliminar equipo {i+1}", key=f"eliminar_{i}"):
        st.session_state.equipos.pop(i)
        st.experimental_rerun()

# --- ENVÍO DE CORREO ---
if st.button("Enviar Registro"):
    if not cliente or not ingeniero or not st.session_state.equipos:
        st.warning("Por favor completa todos los campos y agrega al menos un equipo.")
    else:
        try:
            remitente = "tu_correo@medtronic.com"
            destinatario = "destinatario@medtronic.com"
            asunto = f"{tipo_movimiento} de equipos - {cliente}"

            cuerpo = f"""
            Cliente: {cliente}
            Ingeniero: {ingeniero}
            Tipo de Movimiento: {tipo_movimiento}
            Comentarios: {comentarios}

            Equipos:
            """
            for nombre, serial in st.session_state.equipos:
                cuerpo += f"- {nombre} (Serial: {serial})\n"

            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            msg.attach(MIMEText(cuerpo, 'plain'))

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(remitente, "tu_contraseña")
            server.send_message(msg)
            server.quit()

            st.success("Correo enviado correctamente.")
            # Limpiar campos
            st.session_state.equipos = []
        except Exception as e:
            st.error(f"Error al enviar el correo: {e}")

















