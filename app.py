# app.py
import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

st.set_page_config(page_title="Portal de Certificados", layout="wide")

st.title("Portal de Certificados")

# Subir CSV o usar el existente
csv_path = "data/certificados_streamlit_ready.csv"

try:
    df = pd.read_csv(csv_path, encoding="utf-8")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Convertir columna documento a string
df["documento"] = df["documento"].astype(str)

documento_buscar = st.text_input("Ingrese el número de documento del estudiante")

if documento_buscar:
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s) para este estudiante.")
        
        # Mostrar certificados con botones horizontales
        for index, fila in df_user.iterrows():
            curso_nombre = fila["curso o diplomado"]
            archivo_pdf = generar_certificado(
                nombre=fila.nombre,
                documento=fila.documento,
                curso=curso_nombre,
                horas=fila.horas,
                fecha=fila.fecha,
                facultad=fila.facultad,
                firma_decano=fila.firma_decano,
                nombre_decano=fila.nombre_decano,
                firma_vicerrector=fila.firma_vicerrector,
                nombre_vicerrector=fila.nombre_vicerrector,
                logo_uc="assets/logo_uceva.png",
                output_path=f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"
            )
            
            col1, col2 = st.columns([8,2])
            with col1:
                st.markdown(f"**Curso/Diplomado:** {curso_nombre} ({fila.horas} horas)")
            with col2:
                with open(archivo_pdf, "rb") as f:
                    pdf_bytes = f.read()
                    st.download_button(
                        label="📄 Descargar",
                        data=pdf_bytes,
                        file_name=f"{fila.documento}_{curso_nombre.replace(' ','_')}.pdf",
                        mime="application/pdf",
                    )