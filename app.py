import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# Crear carpeta si no existe
os.makedirs("certificados_generados", exist_ok=True)

st.title("Portal de Certificados")

# Cargar CSV
try:
    df = pd.read_csv("data/certificados_streamlit_ready.csv", sep=';', encoding="utf-8-sig")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Convertir columna documento a str
df["documento"] = df["documento"].astype(str)

documento_buscar = st.text_input("Ingrese el número de documento del estudiante:")

if documento_buscar:
    df_user = df[df["documento"] == documento_buscar.strip()]
    if df_user.empty:
        st.warning("No se encontraron certificados para ese documento")
    else:
        st.write(f"Se encontraron {len(df_user)} certificados para el estudiante.")

        for index, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

            generar_certificado(
                nombre=fila.nombre,
                documento=fila.documento,
                curso=curso_nombre,
                horas=fila.horas,
                fecha=fila.fecha,
                facultad=fila.facultad,
                firma_decano=fila.firma_decano,
                nombre_decano=fila.nombre_decano if pd.notna(fila.nombre_decano) else "",
                cargo_decano=f"Decano(a) Facultad de {fila.facultad}",
                firma_vicerrector=fila.firma_vicerrector,
                nombre_vicerrector=fila.nombre_vicerrector if pd.notna(fila.nombre_vicerrector) else "",
                cargo_vicerrector="Vicerrector Académico",
                output_path=output_file
            )

            with open(output_file, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label=f"📄 Descargar {curso_nombre}",
                    data=pdf_bytes,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )