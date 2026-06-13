# app.py final
import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados - UCEVA")

# Crear carpeta para certificados generados si no existe
os.makedirs("certificados_generados", exist_ok=True)

# Leer CSV
CSV_PATH = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Limpiar nombres de columnas (eliminar espacios invisibles)
df.columns = df.columns.str.strip()
df["documento"] = df["documento"].astype(str)

# Input del documento
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    df_user = df[df["documento"] == documento_input.strip()]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")

        # Botones horizontales
        cols = st.columns(len(df_user))
        for i, fila in enumerate(df_user.itertuples()):
            curso_nombre = getattr(fila, "curso_o_diplomado")
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

            # Generar certificado
            generar_certificado(
                nombre=fila.nombre,
                documento=fila.documento,
                curso=curso_nombre,
                horas=fila.horas,
                fecha=fila.fecha,
                facultad=fila.facultad,
                firma_decano=getattr(fila, "firma_decano", ""),
                nombre_decano=getattr(fila, "nombre_decano", ""),
                firma_vicerrector=getattr(fila, "firma_vicerrector", ""),
                nombre_vicerrector=getattr(fila, "nombre_vicerrector", ""),
                output_path=output_file
            )

            # Botón de descarga
            with cols[i]:
                with open(output_file, "rb") as f:
                    st.download_button(
                        label=f"📄 {curso_nombre}",
                        data=f.read(),
                        file_name=os.path.basename(output_file),
                        mime="application/pdf"
                    )