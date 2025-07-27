import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from PIL import Image

# Configuraciones generales
st.set_page_config(page_title="Registro de Equipos", layout="wide")
st.markdown("<style>body { background-color: #F0F2F6; }</style>", unsafe_allow_html=True)

# Cargar logo
logo_path = "logo_medtronic.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col1:
        st.image(logo_path, width=150)

# Título principal
st.markdown("<h2 style='text-align: center;'>REGISTRO DE EQUIPOS</h2>", unsafe_allow_html=True)

# Datos generales
cliente = st.text_input("Cliente")
ingeniero = st.selectbox("Ingeniero responsable", ["Andrés Ramírez", "Andrés Espinosa", "Carlos Salas", "Santiago Rojas"])

# Diccionario de correos (puedes ampliarlo)
correos_ingenieros = {
    "Andrés Ramírez": "andres.ramirez@medtronic.com",
    "Andrés Espinosa": "andres.espinosa@medtronic.com",
    "Carlos Salas": "carlos.salas@medtronic.com",
    "Santiago Rojas": "santiago.rojas@medtronic.com"
}

# Tipo de movimiento
movimiento = st.radio("Tipo de movimiento", ("Ingreso", "Salida"), horizontal=True)

# Contenedor para equipos
st.markdown("---")
equipos = []
num_equipos = st.number_input("¿Cuántos equipos quieres registrar?", min_value=1, max_value=10, step=1)

for i in range(num_equipos):
    st.subheader(f"Equipo #{i + 1}")
    equipo = {}
    equipo['serial'] = st.text_input(f"Serial del equipo #{i + 1}", key=f"serial_{i}")
    equipo['tipo'] = st.selectbox(f"Tipo de equipo #{i + 1}", ["WEM", "ForceTriad", "FX", "Electrobisturí", "Otros"], key=f"tipo_{i}")
    equipo['observacion'] = st.text_area(f"Observaciones físicas #{i + 1}", key=f"obs_{i}")
    equipo['accesorios'] = st.text_area(f"Accesorios del equipo #{i + 1}", key=f"acc_{i}")
    equipo['imagen'] = st.file_uploader(f"Sube una imagen del equipo #{i + 1}", type=["png", "jpg", "jpeg"], key=f"img_{i}")
    equipos.append(equipo)
    st.markdown("---")

# Función para enviar correo
def enviar_correo():
    from_email = "tu_correo@gmail.com"
    password = "tu_contraseña"
    to_email = correos_ingenieros[ingeniero]

    mensaje = MIMEMultipart()
    mensaje["Subject"] = f"{movimiento.upper()} de equipo(s) - {cliente}"
    mensaje["From"] = from_email
    mensaje["To"] = to_email

    # Crear el cuerpo del mensaje en HTML
    cuerpo_html = f"""
    <h2>{movimiento.upper()} de equipo(s) - {cliente}</h2>
    <p><strong>Ingeniero responsable:</strong> {ingeniero}</p>
    """
    for idx, eq in enumerate(equipos):
        cuerpo_html += f"""
        <hr>
        <h4>Equipo #{idx + 1}</h4>
        <p><strong>Tipo:</strong> {eq['tipo']}</p>
        <p><strong>Serial:</strong> {eq['serial']}</p>
        <p><strong>Observaciones:</strong> {eq['observacion']}</p>
        <p><strong>Accesorios:</strong> {eq['accesorios']}</p>
        """
        if eq['imagen'] is not None:
            img_bytes = eq['imagen'].read()
            imagen = MIMEImage(img_bytes)
            imagen.add_header('Content-ID', f"<imagen{idx}>")
            mensaje.attach(imagen)
            cuerpo_html += f'<img src="cid:imagen{idx}" width="400"><br>'

    mensaje.attach(MIMEText(cuerpo_html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(mensaje)
        st.success("¡Correo enviado exitosamente!")
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")

# Botón de envío
if st.button("Enviar Registro por Correo"):
    if cliente and ingeniero:
        enviar_correo()
    else:
        st.warning("Por favor, completa los campos de cliente e ingeniero.")











