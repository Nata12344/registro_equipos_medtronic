# app.py
import streamlit as st
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io

st.set_page_config(page_title="Registro de Equipo - Medtronic", layout="centered")

# Correos
CORREOS_INGENIEROS = {
    "Nicolle Riaño": "nicolle.n.riano@medtronic.com"
}

# Logo
st.image("logo_medtronic.png", width=200)

# Pantalla de inicio
if "tipo_operacion" not in st.session_state:
    st.session_state.tipo_operacion = None

if st.session_state.tipo_operacion is None:
    st.title("¿Qué deseas registrar?")
    if st.button("Ingreso", use_container_width=True):
        st.session_state.tipo_operacion = "Ingreso"
    if st.button("Salida", use_container_width=True):
        st.session_state.tipo_operacion = "Salida"
    st.stop()

# Datos generales
st.title(f"{st.session_state.tipo_operacion} - Registro de equipos")
cliente = st.text_input("Cliente:")
ingeniero = st.selectbox("Ingeniero:", list(CORREOS_INGENIEROS.keys()))
movimiento = st.text_input("Movimiento / Delivery:")

# Control dinámico de equipos
if "equipos" not in st.session_state:
    st.session_state.equipos = []

if st.button("➕ Agregar nuevo equipo"):
    st.session_state.equipos.append({})

# Renderizar equipos
for i, equipo in enumerate(st.session_state.equipos):
    with st.expander(f"Equipo {i + 1}", expanded=True):
        col1, col2 = st.columns(2)
        tipo = col1.selectbox("Tipo de equipo", ["WEM", "ForceTriad", "FX", "PB840", "PB980", "BIS VISTA", "CONSOLA DE CAMARA"], key=f"tipo_{i}")
        serial = col2.text_input("Serial", key=f"serial_{i}")

        observaciones_opciones = ["Carcasa rayada", "Golpes visibles", "Pantalla rayada", "Pieza rotos", "Cable dañado", "otro"]
        obs_seleccionadas = st.multiselect("Observaciones físicas", observaciones_opciones, key=f"obs_{i}")
        obs_otro = ""
        if "otro" in obs_seleccionadas:
            obs_otro = st.text_input("¿Cuál otra observación?", key=f"otro_{i}")

        llegada_label = "¿Cómo llegó el equipo?" if st.session_state.tipo_operacion == "Ingreso" else "¿Cómo sale el equipo?"
        llegada_formas = ["Caja original", "Caja cartón", "Huacal", "Maletín", "Contenedor"]
        llegada = st.multiselect(llegada_label, llegada_formas, key=f"llegada_{i}")

        accesorios = st.text_input("Accesorios:", key=f"accesorios_{i}")
        fotos = st.file_uploader("Fotos del equipo (mínimo 4)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key=f"fotos_{i}")

# Botón para enviar
if st.button("📤 Enviar reporte"):

    errores = []
    for i in range(len(st.session_state.equipos)):
        fotos = st.session_state[f"fotos_{i}"]
        if len(fotos) < 4:
            errores.append(f"Equipo {i + 1} debe tener al menos 4 fotos.")
    
    if not ingeniero:
        errores.append("Debes seleccionar un ingeniero.")
    
    if errores:
        for error in errores:
            st.error(error)
        st.stop()

    # Construir y enviar correo
    try:
        from_email = "rianonicolle1101@gmail.com"
        password = "pmfb qjwu rnyc bojy"
        to_emails = [CORREOS_INGENIEROS[ingeniero], "mejiah5@medtronic.com"]

        msg = MIMEMultipart('related')
        msg["From"] = from_email
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = f"{st.session_state.tipo_operacion} ST - Movimiento: {movimiento}"

        cuerpo_html = f"<html><body><h3>{st.session_state.tipo_operacion} de equipos</h3><p><b>Cliente:</b> {cliente}<br><b>Ingeniero:</b> {ingeniero}<br><b>Movimiento:</b> {movimiento}</p>"

        cid_counter = 0
        imagenes = []

        for i in range(len(st.session_state.equipos)):
            tipo = st.session_state[f"tipo_{i}"]
            serial = st.session_state[f"serial_{i}"]
            obs = st.session_state[f"obs_{i}"]
            llegada = st.session_state[f"llegada_{i}"]
            accesorios = st.session_state[f"accesorios_{i}"]
            fotos = st.session_state[f"fotos_{i}"]
            obs_otro = st.session_state[f"otro_{i}"] if "otro" in obs else ""

            cuerpo_html += f"<p><b>Equipo {i+1}:</b><br>- Tipo: {tipo}<br>- Serial: {serial}<br>- Accesorios: {accesorios}<br>- Observaciones: {', '.join(obs)} {obs_otro}<br>- Llegada/Salida: {', '.join(llegada)}<br>"

            for foto in fotos:
                cid = f"img{cid_counter}"
                cid_counter += 1
                cuerpo_html += f'<img src="cid:{cid}" style="max-width:300px;"><br>'
                img = MIMEImage(foto.read())
                img.add_header('Content-ID', f'<{cid}>')
                img.add_header('Content-Disposition', 'inline', filename=foto.name)
                imagenes.append(img)

            cuerpo_html += "</p>"

        cuerpo_html += "<p><i>Este mensaje ha sido generado automáticamente por el Departamento de Servicio Técnico de Medtronic.</i></p></body></html>"
        msg.attach(MIMEText(cuerpo_html, "html"))

        for img in imagenes:
            msg.attach(img)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()

        st.success("✅ Correo enviado correctamente")
        st.balloons()
        st.session_state.tipo_operacion = None
        st.session_state.equipos = []

    except Exception as e:
        st.error(f"❌ Error al enviar: {e}")


