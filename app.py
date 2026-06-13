import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

st.set_page_config(page_title="Portal de Certificados", layout="centered")
st.title("Portal de Certificados - UCEVA")

# Leer CSV con la ruta correcta
CSV_PATH = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", sep=';')
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Ingreso del documento
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    # Filtrar por documento
    df_user = df[df["documento"].astype(str) == documento_input.strip()]
    
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")
        cols = st.columns(len(df_user))  # Botones horizontales

        for i, fila in enumerate(df_user.itertuples()):
            with cols[i]:
                curso_nombre = getattr(fila, "curso_o_diplomado")
                archivo_pdf = generar_certificado(
                    nombre=fila.nombre,
                    documento=fila.documento,
                    curso=curso_nombre,
                    horas=fila.horas,
                    fecha=fila.fecha,
                    facultad=fila.facultad,
                    firma_decano_path=fila.firma_decano,
                    nombre_decano=fila.nombre_decano if hasattr(fila, 'nombre_decano') else "",
                    firma_vicerrector_path=fila.firma_vicerrector,
                    nombre_vicerrector=fila.nombre_vicerrector if hasattr(fila, 'nombre_vicerrector') else "",
                    logo_path="assets/logo_uceva.png",
                    output_path=f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"
                )
                st.download_button(
                    label=f"📄 Descargar: {curso_nombre}",
                    data=open(archivo_pdf, "rb").read(),
                    file_name=f"{fila.documento}_{curso_nombre.replace(' ','_')}.pdf",
                    mime="application/pdf"
                )