import streamlit as st

# Mostrar el logo alineado a la izquierda usando HTML
st.markdown("""
    <div style="text-align: left;">
        <img src="https://i.imgur.com/DF7gkTe.png" alt="Medtronic Logo" width="150">
    </div>
""", unsafe_allow_html=True)

# Línea divisoria
st.markdown("---")

# Título
st.markdown("<h2 style='text-align: center; color: #003366;'>¿Qué deseas registrar?</h2>", unsafe_allow_html=True)

# Radio buttons
opcion = st.radio("", ["Ingreso", "Salida"], horizontal=True)

# Botón continuar
if st.button("Continuar"):
    st.success(f"Seleccionaste: {opcion}")










