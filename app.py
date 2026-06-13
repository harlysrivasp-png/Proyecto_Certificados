# app.py
import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado

# Configuración de la página
st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("📄 Portal de Certificados - UCEVA")

# Leer CSV con ruta absoluta y codificación UTF-8
csv_path = "/data/certificados_final_utf8.csv"
try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig", sep=";")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Ingreso del documento del estudiante
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    # Filtrar certificados por documento
    resultados = df[df['documento'].astype(str) == documento_input.strip()]
    
    if resultados.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(resultados)} certificado(s) para este estudiante.")

        # Crear columnas para botones horizontales
        col_buttons = st.columns(len(resultados))

        # Iterar sobre cada certificado
        for idx, (i, fila) in enumerate(resultados.iterrows()):
            with col_buttons[idx]:
                archivo_pdf = generar_certificado(
                    nombre=fila["nombre"],
                    documento=fila["documento"],
                    programa=fila["programa"],
                    horas=fila["horas"],
                    fecha=fila["fecha"],
                    logo=fila.get("logo", "assets/logo_default.png"),
                    firma_decano=fila.get("firma_decano", "assets/firma_decano_default.png"),
                    cargo_decano=fila.get("cargo_decano", "Decano/a"),
                    firma_vicerrector=fila.get("firma_vicerrector", "assets/firma_vicerrector_default.png"),
                    cargo_vicerrector=fila.get("cargo_vicerrector", "Vicerrector/a")
                )

                st.download_button(
                    label=f"📄 Descargar: {fila['programa']}",
                    data=open(archivo_pdf, "rb").read(),
                    file_name=f"certificado_{fila['documento']}_{fila['programa'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key=f"download_{idx}"
                )