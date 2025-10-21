import pandas as pd
from fpdf import FPDF

# Valor de BPC actualizado 2025
BPC = 6576

# Escalas IRPF (anuales)
IRPF_ESCALAS = [
    (0, 7*BPC, 0.0),
    (7*BPC, 10*BPC, 0.10),
    (10*BPC, 15*BPC, 0.15),
    (15*BPC, 30*BPC, 0.24),
    (30*BPC, 50*BPC, 0.25),
    (50*BPC, 75*BPC, 0.27),
    (75*BPC, 115*BPC, 0.31),
    (115*BPC, float("inf"), 0.36)
]

def calcular_irpf(sueldo_anual):
    for inicio, fin, tasa in IRPF_ESCALAS:
        if inicio <= sueldo_anual <= fin:
            return sueldo_anual * tasa / 12  # Mensual
    return 0.0

def calcular_bps(sueldo_base):
    jubilacion = sueldo_base * 0.15
    fonasa = sueldo_base * 0.07  # promedio general
    frl = sueldo_base * 0.00125
    return jubilacion, fonasa, frl

def calcular_liquidacion(sueldo_base, horas_extras, valor_hora_extra, hijos=0, hijos_discapacidad=0):
    sueldo_bruto = sueldo_base + (horas_extras * valor_hora_extra)
    
    # BPS
    jubilacion, fonasa, frl = calcular_bps(sueldo_bruto)
    
    # IRPF
    irpf_base = calcular_irpf(sueldo_bruto)
    deduccion_hijos = hijos * 20*BPC/12
    deduccion_hijos_disc = hijos_discapacidad * 40*BPC/12
    irpf = max(irpf_base - deduccion_hijos - deduccion_hijos_disc, 0)
    
    # Sueldo neto
    sueldo_neto = sueldo_bruto - jubilacion - fonasa - frl - irpf
    
    data = {
        "Sueldo Base": [sueldo_base],
        "Horas Extras": [horas_extras],
        "Valor Hora Extra": [valor_hora_extra],
        "Sueldo Bruto": [sueldo_bruto],
        "Jubilación (BPS)": [jubilacion],
        "FONASA": [fonasa],
        "FRL": [frl],
        "IRPF": [irpf],
        "Sueldo Neto": [sueldo_neto]
    }
    
    df = pd.DataFrame(data)
    return df

def exportar_pdf(df_row, nombre):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Liquidación de sueldo - {nombre}", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    
    for key, val in df_row.items():
        pdf.cell(200, 10, f"{key}: {val:.2f}", ln=True)
    
    file = f"liquidacion_{nombre}.pdf"
    pdf.output(file)
    return file
