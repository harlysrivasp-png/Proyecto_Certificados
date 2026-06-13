# app.py
import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados UCEVA")

# Carpeta de salida
os.makedirs("certificados_generados", exist_ok=True)

# Cargar CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

df["documento"] = df["documento"].astype(str)

# Input de documento
documento_input = st.text_input("Ingrese el número de documento del estudiante:")

if documento_input:
    df_user = df[df["documento"] == documento_input.strip()]
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificados para este estudiante.")

        for idx, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila['documento']}_{curso_nombre.replace(' ','_')}.pdf"

            # Validar rutas de imágenes existentes
            logo = "assets/logo.jpg" if os.path.exists("assets/logo.jpg") else None
            plantilla_fondo = "assets/plantilla_fondo.png" if os.path.exists("assets/plantilla_fondo.png") else None
            firma_decano = fila["firma_decano"] if os.path.exists(fila["firma_decano"]) else None
            firma_vicerrector = fila["firma_vicerrector"] if os.path.exists(fila["firma_vicerrector"]) else None

            # Generar certificado
            generar_certificado(
                nombre=fila.get("nombre",""),
                documento=fila.get("documento",""),
                curso_o_diplomado=curso_nombre,
                horas=fila.get("horas",""),
                fecha=fila.get("fecha",""),
                facultad=fila.get("facultad",""),
                logo=logo,
                plantilla_fondo=plantilla_fondo,
                firma_decano=firma_decano,
                nombre_decano=fila.get("nombre_decano",""),
                firma_vicerrector=firma_vicerrector,
                nombre_vicerrector=fila.get("nombre_vicerrector",""),
                output_path=output_file
            )

            st.write(f"**Certificado:** {curso_nombre}")
            with open(output_file, "rb") as f:
                st.download_button(
                    label=f"📄 Descargar {curso_nombre}",
                    data=f.read(),
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )