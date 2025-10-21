import streamlit as st
import pandas as pd
from database import create_db, get_session, Empleado
from utils import calcular_liquidacion, exportar_excel, exportar_pdf

st.set_page_config(page_title="Sistema de Sueldos", page_icon="💰")

st.title("💼 Sistema de Liquidación de Sueldos")

# Inicializar base de datos
create_db()
session = get_session()

menu = st.sidebar.selectbox("Menú", ["Liquidar sueldo", "Historial de empleados"])

if menu == "Liquidar sueldo":
    with st.form("liquidar"):
        nombre = st.text_input("Nombre del empleado")
        cargo = st.text_input("Cargo / Puesto")
        sueldo_base = st.number_input("Sueldo base ($)", min_value=0.0)
        horas_extras = st.number_input("Horas extras", min_value=0)
        valor_hora_extra = st.number_input("Valor por hora extra ($)", value=300.0)
        presentismo = st.checkbox("Aplica presentismo (10%)", value=True)
        submit = st.form_submit_button("Calcular")

    if submit:
        neto, extras, bonus, descuentos = calcular_liquidacion(sueldo_base, horas_extras, valor_hora_extra, presentismo)

        df = pd.DataFrame({
            "Empleado": [nombre],
            "Cargo": [cargo],
            "Sueldo base": [sueldo_base],
            "Horas extras": [extras],
            "Presentismo": [bonus],
            "Descuentos": [descuentos],
            "Neto a cobrar": [neto],
        })

        st.subheader("🧾 Resultado de la liquidación")
        st.dataframe(df)

        # Guardar en DB
        nuevo = Empleado(
            nombre=nombre, cargo=cargo, sueldo_base=sueldo_base,
            horas_extras=horas_extras, valor_hora_extra=valor_hora_extra,
            presentismo=presentismo, neto=neto
        )
        session.add(nuevo)
        session.commit()

        # Exportar
        excel = exportar_excel(df, nombre)
        pdf = exportar_pdf(df.iloc[0], nombre)

        st.download_button("📥 Descargar Excel", open(excel, "rb").read(), file_name=excel)
        st.download_button("📄 Descargar PDF", open(pdf, "rb").read(), file_name=pdf)

elif menu == "Historial de empleados":
    empleados = session.query(Empleado).all()
    if empleados:
        data = [{
            "Nombre": e.nombre,
            "Cargo": e.cargo,
            "Sueldo base": e.sueldo_base,
            "Horas extras": e.horas_extras,
            "Neto a cobrar": e.neto
        } for e in empleados]
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.download_button("📦 Exportar historial a Excel", df.to_csv(index=False), file_name="historial.csv")
    else:
        st.info("No hay empleados registrados aún.")
