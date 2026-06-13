# app.py
import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados - UCEVA")

# Carpeta para certificados generados
os.makedirs("certificados_generados", exist_ok=True)

# Leer CSV
try:
    df = pd.read_csv("data/certificados_streamlit_ready.csv", sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Convertir documento a string
df["documento"] = df["documento"].astype(str)

# Input del usuario
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    df_user = df[df["documento"] == documento_input.strip()]
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} curso(s) para este documento.")

        for idx, fila in df_user.iterrows():
            curso_nombre = str(fila["curso_o_diplomado"])
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

            # Generar certificado
            generar_certificado(
                nombre=str(fila.nombre),
                documento=str(fila.documento),
                curso=curso_nombre,
                horas=str(fila.horas),
                fecha=str(fila.fecha),
                facultad=str(fila.facultad),
                firma_decano=str(fila.firma_decano),
                nombre_decano=str(fila.nombre_decano),
                cargo_decano=f"Decano(a) Facultad de {fila.facultad}",
                firma_vicerrector=str(fila.firma_vicerrector),
                nombre_vicerrector=str(fila.nombre_vicerrector),
                cargo_vicerrector="Vicerrector Académico",
                output_path=output_file
            )

            st.markdown(f"**Certificado: {curso_nombre}**")
            with open(output_file, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label=f"📄 Descargar {curso_nombre}",
                    data=pdf_bytes,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )