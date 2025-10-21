import pandas as pd
from fpdf import FPDF

def calcular_liquidacion(sueldo_base, horas_extras, valor_hora_extra, presentismo):
    extras = horas_extras * valor_hora_extra
    bonus = sueldo_base * 0.1 if presentismo else 0
    bps = sueldo_base * 0.15
    irpf = sueldo_base * 0.08
    neto = sueldo_base + extras + bonus - (bps + irpf)
    return neto, extras, bonus, -(bps + irpf)

def exportar_excel(df, nombre):
    file = f"liquidacion_{nombre}.xlsx"
    df.to_excel(file, index=False)
    return file

def exportar_pdf(df, nombre):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Liquidación de sueldo - {nombre}", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    for key, val in df.items():
        pdf.cell(200, 10, f"{key}: {val[0]}", ln=True)
    file = f"liquidacion_{nombre}.pdf"
    pdf.output(file)
    return file
