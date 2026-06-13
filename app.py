import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# Crear carpeta de salida si no existe
os.makedirs("certificados_generados", exist_ok=True)

st.title("Portal de Certificados")

# Cargar CSV
try:
    df = pd.read_csv("data/certificados_streamlit_ready.csv", sep=';', encoding="utf-8-sig').fillna("")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Solicitar documento del estudiante
documento_buscar = st.text_input("Ingrese el número de documento del estudiante:")

if documento_buscar:
    # Filtrar por documento
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_buscar.strip()]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.write(f"Se encontraron {len(df_user)} certificado(s)")

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

            st.success(f"Certificado generado: {output_file}")
            with open(output_file, "rb") as pdf_file:
                st.download_button(
                    label=f"📄 Descargar certificado: {curso_nombre}",
                    data=pdf_file.read(),
                    file_name=output_file.split("/")[-1],
                    mime="application/pdf"
                )