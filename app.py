import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

# Crear carpeta de salida si no existe
if not os.path.exists("certificados_generados"):
    os.makedirs("certificados_generados")

st.title("Portal de Certificados - UCEVA")

# Cargar CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Convertir documento a string
df["documento"] = df["documento"].astype(str)

# Input del usuario
documento_buscar = st.text_input("Ingrese su número de documento:")

if documento_buscar:
    # Filtrar por documento
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron registros para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} curso(s) para este documento.")
        for index, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

            # Generar el certificado
            generar_certificado(
                nombre=fila["nombre"],
                documento=fila["documento"],
                curso=curso_nombre,
                horas=fila["horas"],
                fecha=fila["fecha"],
                facultad=fila["facultad"],
                firma_decano=fila["firma_decano"],
                nombre_decano=fila["nombre_decano"],
                firma_vicerrector=fila["firma_vicerrector"],
                nombre_vicerrector=fila["nombre_vicerrector"],
                output_path=output_file
            )

            # Botón de descarga
            with open(output_file, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label=f"📄 Descargar Certificado - {curso_nombre}",
                    data=pdf_bytes,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )