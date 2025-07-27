import streamlit as st

# Mostrar el logo un poco más a la izquierda
col1, col2, col3 = st.columns([2, 1, 3])  # Cambia los anchos de columna

with col1:
    st.image("logo_medtronic.png", width=150)  # Ajusta el tamaño si deseas

with col2:
    st.empty()

with col3:
    st.empty()

# Línea divisoria
st.markdown("---")

# Título
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Opción de selección
opcion = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón de continuar
if st.button("Continuar"):
    st.write(f"Seleccionaste: {opcion}")










