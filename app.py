import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

st.set_page_config(page_title="Portal de Certificados", layout="centered")

st.title("Portal de Certificados - UCEVA")

# Ruta del CSV
CSV_PATH = "data/certificados_streamlit_ready.csv"

# Leer CSV con manejo de errores
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Input de documento
documento_buscar = st.text_input("Ingrese el número de documento del estudiante")

if documento_buscar:
    df_user = df[df["documento"].astype(str) == documento_buscar]
    
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")
        col_layout = st.columns(len(df_user))  # Botones horizontales

        for i, fila in enumerate(df_user.itertuples()):
            with col_layout[i]:
                archivo_pdf = generar_certificado(
                    nombre=fila.nombre,
                    documento=fila.documento,
                    curso=fila.curso_o_diplomado,
                    horas=fila.horas,
                    fecha=fila.fecha,
                    facultad=fila.facultad,
                    firma_decano_path=fila.firma_decano,
                    nombre_decano=fila.nombre_decano,
                    firma_vicerrector_path=fila.firma_vicerrector,
                    nombre_vicerrector=fila.nombre_vicerrector,
                    logo_path="assets/logo_uceva.png",
                    output_path=f"certificados_generados/{fila.documento}_{fila.curso_o_diplomado}.pdf"
                )

                st.download_button(
                    label=f"📄 Descargar: {fila.curso_o_diplomado}",
                    data=open(archivo_pdf, "rb").read(),
                    file_name=f"{fila.documento}_{fila.curso_o_diplomado}.pdf",
                    mime="application/pdf"
                )