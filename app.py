# app.py
import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")

st.title("Portal de Certificados")

# Leer CSV con codificación utf-8-sig
df = pd.read_csv("certificados.csv", encoding="utf-8-sig")  
# columnas esperadas: nombre, documento, programa, horas, fecha, logo, firma_decano, cargo_decano, firma_vicerrector, cargo_vicerrector

documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    resultados = df[df['documento'].astype(str) == documento_input]
    if resultados.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(resultados)} certificado(s).")
        # Botones en horizontal usando columnas
        col_buttons = st.columns(len(resultados))
        for idx, (i, fila) in enumerate(resultados.iterrows()):
            with col_buttons[idx]:
                archivo_pdf = generar_certificado(
                    nombre=fila.nombre,
                    documento=fila.documento,
                    programa=fila.programa,
                    horas=fila.horas,
                    fecha=fila.fecha,
                    logo=fila.get("logo", "assets/logo_default.png"),
                    firma_decano=fila.get("firma_decano", "assets/firma_decano_default.png"),
                    cargo_decano=fila.get("cargo_decano", "Decano"),
                    firma_vicerrector=fila.get("firma_vicerrector", "assets/firma_vicerrector_default.png"),
                    cargo_vicerrector=fila.get("cargo_vicerrector", "Vicerrector")
                )
                st.download_button(
                    label=f"📄 Descargar Certificado {idx+1}",
                    data=archivo_pdf,
                    file_name=f"certificado_{fila.documento}.pdf",
                    mime="application/pdf"
                )