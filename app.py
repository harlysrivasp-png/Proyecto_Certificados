import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")

st.title("Portal de Certificados")

# Leer CSV
try:
    df = pd.read_csv("data/certificados_streamlit_ready.csv", sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Input documento
documento_buscar = st.text_input("Ingrese el número de documento del estudiante:")

if documento_buscar:
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.write(f"Se encontraron {len(df_user)} certificado(s) para este estudiante:")

        for idx, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]

            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

            generar_certificado(
                nombre=fila.nombre,
                documento=fila.documento,
                curso_o_diplomado=curso_nombre,
                horas=fila.horas,
                fecha=fila.fecha,
                facultad=fila.facultad,
                firma_decano=fila.firma_decano,
                nombre_decano=fila.nombre_decano,
                firma_vicerrector=fila.firma_vicerrector,
                nombre_vicerrector=fila.nombre_vicerrector,
                output_path=output_file
            )

            with open(output_file, "rb") as f:
                st.download_button(
                    label=f"📄 Descargar certificado: {curso_nombre}",
                    data=f,
                    file_name=f"{fila.documento}_{curso_nombre.replace(' ','_')}.pdf",
                    mime="application/pdf"
                )