import streamlit as st
import pandas as pd
from utils import calcular_liquidacion, exportar_pdf
from database import create_db, get_session, Empleado

# Conectar base de datos
create_db()
session = get_session()

st.title("💼 Sistema de Liquidación de Sueldos - Uruguay")

# Formulario de ingreso de empleado
with st.form("empleado_form"):
    nombre = st.text_input("Nombre del empleado")
    cargo = st.text_input("Cargo / Puesto")
    sueldo_base = st.number_input("Sueldo base ($)", min_value=0.0, value=150000.0)
    horas_extras = st.number_input("Horas extras", min_value=0)
    valor_hora_extra = st.number_input("Valor por hora extra ($)", min_value=0.0, value=1000.0)
    hijos = st.number_input("Cantidad de hijos", min_value=0)
    hijos_discapacidad = st.number_input("Cantidad de hijos con discapacidad", min_value=0)
    submitted = st.form_submit_button("Calcular Liquidación")

if submitted:
    # Calcular liquidación
    df = calcular_liquidacion(
        sueldo_base, horas_extras, valor_hora_extra,
        hijos, hijos_discapacidad
    )

    st.subheader("🧾 Resultado de la liquidación")
    st.dataframe(df)

    # Exportar PDF
    pdf_file = exportar_pdf(df.iloc[0], nombre)
    st.download_button("Descargar PDF", pdf_file, file_name=f"Liquidacion_{nombre}.pdf")

    # Guardar en base de datos
    empleado = Empleado(
        nombre=nombre,
        cargo=cargo,
        sueldo_base=sueldo_base,
        horas_extras=horas_extras,
        valor_hora_extra=valor_hora_extra,
        hijos=hijos,
        hijos_discapacidad=hijos_discapacidad,
        sueldo_neto=df["Sueldo Neto"][0]
    )
    session.add(empleado)
    session.commit()
