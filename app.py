import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# Título de la app
st.title("Portal de Certificados")
st.write("Genera y descarga tus certificados automáticamente")

# Crear carpeta para certificados generados
if not os.path.exists("certificados_generados"):
    os.makedirs("certificados_generados")

# Leer CSV
CSV_PATH = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Input del usuario
documento_buscar = st.text_input("Ingresa tu número de documento:")

if documento_buscar:
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")

        # Botones horizontales para descargar cada certificado
        cols = st.columns(len(df_user))
        for i, fila in enumerate(df_user.itertuples()):
            curso_nombre = getattr(fila, "curso o diplomado")  # columna CSV
            archivo_pdf = generar_certificado(
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
                output_path=f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"
            )

            # Botón de descarga
            with cols[i]:
                with open(archivo_pdf, "rb") as f:
                    st.download_button(
                        label=f"📄 {curso_nombre}",
                        data=f.read(),
                        file_name=os.path.basename(archivo_pdf),
                        mime="application/pdf"
                    )