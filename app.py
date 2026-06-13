import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

st.title("Portal de Certificados UCEVA")

# Leer CSV
csv_path = "data/certificados_streamlit_ready.csv"
if not os.path.exists(csv_path):
    st.error(f"No se encontró el archivo CSV en {csv_path}")
    st.stop()

df = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig").fillna("")

documento_buscar = st.text_input("Ingrese el número de documento")

if documento_buscar:
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento")
    else:
        st.subheader("Certificados disponibles:")

        for i, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila['documento']}_{curso_nombre.replace(' ','_')}.pdf"
            os.makedirs("certificados_generados", exist_ok=True)

            # Generar certificado
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

            # Botón para descargar
            with open(output_file, "rb") as f:
                btn = st.download_button(
                    label=f"📄 Descargar {curso_nombre}",
                    data=f,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )