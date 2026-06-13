import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados - UCEVA")

# Carpeta para certificados generados
os.makedirs("certificados_generados", exist_ok=True)

# Leer CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Convertir documento a string
df["documento"] = df["documento"].astype(str)

# Input del usuario
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    df_user = df[df["documento"] == documento_input.strip()]

    if df_user.empty:
        st.warning("No se encontraron registros para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} curso(s) para este documento.")

        # Crear botones horizontales para cada certificado
        cols = st.columns(len(df_user))
        for i, fila in enumerate(df_user.itertuples()):
            curso_nombre = getattr(fila, "curso_o_diplomado")
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ', '_')}.pdf"

            # Generar certificado
            generar_certificado(
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
                output_path=output_file
            )

            # Botón de descarga
            with cols[i]:
                with open(output_file, "rb") as pdf_file:
                    st.download_button(
                        label=f"📄 Descargar certificado: {curso_nombre}",
                        data=pdf_file.read(),
                        file_name=os.path.basename(output_file),
                        mime="application/pdf"
                    )