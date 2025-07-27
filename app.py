import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

st.set_page_config(page_title="Registro de Equipos", page_icon="🛠️", layout="centered")

st.title("📦 Registro y Envío de Equipos")

with st.form(key='formulario'):
    st.subheader("Información general")
    ingeniero = st.text_input("Nombre del Ingeniero")
    cliente = st.text_input("Cliente o Hospital")
    tipo_equipo = st.selectbox("Tipo de Equipo", ["WEM", "ForceTriad", "FX", "Otro"])
    numero_serial = st.text_input("Número de Serie")

    st.subheader("Fotos del equipo")
    imagen_entrada = st.file_uploader("Foto de Entrada", type=["png", "jpg", "jpeg"])
    imagen_salida = st.file_uploader("Foto de Salida", type=["png", "jpg", "jpeg"])

    enviar = st.form_submit_button("📨 Enviar correo")

if enviar:
    if not all([ingeniero, cliente, tipo_equipo, numero_serial, imagen_entrada, imagen_salida]):
        st.error("❌ Todos los campos son obligatorios.")
    else:
        try:
            remitente = "tucorreo@gmail.com"  # <-- cámbialo
            contraseña = "tupassword"         # <-- cámbialo o usa secrets
            destinatario = "destino@gmail.com"  # <-- cámbialo

            asunto = f"Envío de equipo: {tipo_equipo}"
            cuerpo = f"""
            <h3>Reporte de Movimiento de Equipo</h3>
            <p><strong>Ingeniero:</strong> {ingeniero}</p>
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Tipo de Equipo:</strong> {tipo_equipo}</p>
            <p><strong>Serial:</strong> {numero_serial}</p>
            """

            mensaje = MIMEMultipart()
            mensaje['From'] = remitente
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto
            mensaje.attach(MIMEText(cuerpo, 'html'))

            # Adjuntar imágenes
            for imagen, nombre in zip([imagen_entrada, imagen_salida], ["entrada", "salida"]):
                img_data = imagen.read()
                imagen_mime = MIMEImage(img_data, name=f"{nombre}.jpg")
                mensaje.attach(imagen_mime)

            # Enviar correo
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
            servidor.quit()

            st.success("✅ Correo enviado exitosamente.")
        except Exception as e:
            st.error(f"⚠️ Error al enviar el correo: {e}")



