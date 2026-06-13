import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# Configuración de página
st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados - UCEVA")

# Leer CSV
CSV_PATH = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", sep=';')
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Ingreso del documento
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    df_user = df[df["documento"].astype(str) == documento_input.strip()]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")
        cols = st.columns(len(df_user))  # Botones horizontales

        for i, fila in enumerate(df_user.itertuples()):
            with cols[i]:
                curso_nombre = getattr(fila, "curso_o_diplomado")
                # Manejo de nombres vacíos
                nombre_decano = str(getattr(fila, "nombre_decano", "") or "")
                nombre_vicerrector = str(getattr(fila, "nombre_vicerrector", "") or "")

                # Generar certificado en memoria (BytesIO)
                archivo_pdf = generar_certificado(
                    nombre=fila.nombre,
                    documento=fila.documento,
                    curso=curso_nombre,
                    horas=fila.horas,
                    fecha=fila.fecha,
                    facultad=fila.facultad,
                    firma_decano_path=fila.firma_decano,
                    nombre_decano=nombre_decano,
                    firma_vicerrector_path=fila.firma_vicerrector,
                    nombre_vicerrector=nombre_vicerrector,
                    logo_path="assets/logo_uceva.png",
                    output_path=None  # No guardamos en disco, solo memoria
                )

                st.download_button(
                    label=f"📄 Descargar: {curso_nombre}",
                    data=archivo_pdf,  # BytesIO directamente
                    file_name=f"{fila.documento}_{curso_nombre.replace(' ','_')}.pdf",
                    mime="application/pdf"
                )