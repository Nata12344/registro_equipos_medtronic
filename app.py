import streamlit as st
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

# Configuración inicial
st.set_page_config(layout="wide")
st.title("Registro de Equipos")

# Diccionario con correos de ingenieros
correos_ingenieros = {
    "Nicolle Riaño": "nicolle.n.riano@medtronic.com",
    "Otro Ingeniero": "otro@medtronic.com"
}

# Sidebar con encabezado
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Medtronic_logo.svg/2560px-Medtronic_logo.svg.png",
        width=200,
    )
    st.markdown(
        f"### {'Ingreso' if 'tipo_operacion' not in st.session_state else st.session_state.tipo_operacion} - Registro de equipos"
    )
    st.markdown(
        "**Información confidencial**  
        Uso exclusivo de Medtronic"
    )

# Operación
tipo_operacion = st.radio("Selecciona el tipo de operación:", ["Ingreso", "Salida"])
st.session_state.tipo_operacion = tipo_operacion

# Formulario
cliente = st.text_input("Cliente (hospital o Medtronic)")
ingeniero = st.selectbox("Ingeniero responsable", list(correos_ingenieros.keys()))
equipos = []

st.markdown("### Agregar equipos")

# Para almacenar info de equipos
if "lista_equipos" not in st.session_state:
    st.session_state.lista_equipos = []

col1, col2 = st.columns(2)
with col1:
    tipo_equipo = st.text_input("Tipo de equipo")
    serial = st.text_input("Número de serie")
with col2:
    foto_entrada = st.file_uploader("Foto del equipo", type=["png", "jpg", "jpeg"])

if st.button("Agregar equipo"):
    if tipo_equipo and serial and foto_entrada:
        st.session_state.lista_equipos.append({
            "tipo": tipo_equipo,
            "serial": serial,
            "foto": foto_entrada
        })
        st.success("Equipo agregado correctamente.")
    else:
        st.warning("Por favor, completa todos los campos.")

# Mostrar lista de equipos agregados
if st.session_state.lista_equipos:
    st.markdown("### Equipos agregados")
    for idx, equipo in enumerate(st.session_state.lista_equipos):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{equipo['tipo']}** - Serial: {equipo['serial']}")
        with col2:
            if st.button("Eliminar", key=f"eliminar_{idx}"):
                st.session_state.lista_equipos.pop(idx)
                st.experimental_rerun()

# Enviar correo
if st.button("Enviar correo"):
    if not cliente or not ingeniero or not st.session_state.lista_equipos:
        st.error("Completa todos los campos antes de enviar.")
    else:
        try:
            msg = MIMEMultipart("related")
            msg["Subject"] = f"{tipo_operacion} de equipo - {cliente}"
            msg["From"] = "tucorreo@dominio.com"
            msg["To"] = correos_ingenieros[ingeniero]

            # HTML del correo
            html = f"""<html><body>
            <p><b>{tipo_operacion} a Servicio Técnico</b></p>
            <p><b>Cliente:</b> {cliente}<br>
            <b>Ingeniero:</b> {ingeniero}</p>
            <p><b>Equipos:</b></p><ul>"""

            for i, equipo in enumerate(st.session_state.lista_equipos):
                cid = f"image{i}"
                html += f"<li>{equipo['tipo']} - Serial: {equipo['serial']}<br><img src='cid:{cid}' width='300'></li><br>"

                # Agregar imagen embebida
                img_data = equipo["foto"].read()
                image = MIMEImage(img_data, name=equipo["foto"].name)
                image.add_header("Content-ID", f"<{cid}>")
                msg.attach(image)

            html += "</ul></body></html>"
            msg.attach(MIMEText(html, "html"))

            # Envío del correo
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("tucorreo@dominio.com", "tu_contraseña")
            server.send_message(msg)
            server.quit()

            st.success("Correo enviado correctamente.")
            st.session_state.lista_equipos.clear()
        except Exception as e:
            st.error(f"Ocurrió un error al enviar el correo: {e}")





















