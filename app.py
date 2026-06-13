# app.py
import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados - UCEVA")

# Crear carpeta para certificados generados
os.makedirs("certificados_generados", exist_ok=True)

# Leer CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig').fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Mostrar input para documento
documento_input = st.text_input("Ingrese su número de documento:")

if documento_input:
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_input.strip()]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificados para {df_user.iloc[0]['nombre']}.")

        for idx, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila['documento']}_{curso_nombre.replace(' ','_')}.pdf"

            # Validar que los archivos de logo y firmas existan
            logo_path = "assets/logo_uceva.png"
            plantilla_fondo = "assets/plantilla_fondo.png"
            if not os.path.exists(logo_path):
                st.error(f"No se encontró el logo en {logo_path}")
                continue
            if not os.path.exists(fila["firma_decano"]):
                st.error(f"No se encontró la firma del decano: {fila['firma_decano']}")
                continue
            if not os.path.exists(fila["firma_vicerrector"]):
                st.error(f"No se encontró la firma del vicerrector: {fila['firma_vicerrector']}")
                continue

            # Generar certificado
            generar_certificado(
                nombre=fila["nombre"],
                documento=fila["documento"],
                curso=fila["curso_o_diplomado"],
                horas=fila["horas"],
                fecha=fila["fecha"],
                facultad=fila["facultad"],
                firma_decano=fila["firma_decano"],
                nombre_decano=fila["nombre_decano"],
                firma_vicerrector=fila["firma_vicerrector"],
                nombre_vicerrector=fila["nombre_vicerrector"],
                logo_uceva=logo_uceva,
                plantilla_fondo=plantilla_fondo,
                output_path=output_file
            )

            # Botón para descargar
            with open(output_file, "rb") as f:
                st.download_button(
                    label=f"📄 Descargar certificado de {curso_nombre}",
                    data=f,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )