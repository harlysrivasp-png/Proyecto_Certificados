import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("Portal de Certificados UCEVA")

# Carpeta de salida
os.makedirs("certificados_generados", exist_ok=True)

# Leer CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Convertir documento a string
if "documento" not in df.columns:
    st.error("El CSV debe tener la columna 'documento'")
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
            # Valores por defecto
            curso_nombre = fila.get("curso_o_diplomado", "Curso Desconocido")
            horas = fila.get("horas", "0")
            fecha = fila.get("fecha", "")
            facultad = fila.get("facultad", "")
            nombre = fila.get("nombre", "")
            nombre_decano = fila.get("nombre_decano", "")
            nombre_vicerrector = fila.get("nombre_vicerrector", "")

            # Validar rutas de imágenes
            logo = "assets/logo_uceva.png"
            plantilla_fondo = "assets/plantilla_fondo.png"
            firma_decano = fila.get("firma_decano", "")
            firma_vicerrector = fila.get("firma_vicerrector", "")

            if not os.path.exists(logo):
                logo = None
            if not os.path.exists(plantilla_fondo):
                plantilla_fondo = None
            if not os.path.exists(firma_decano):
                firma_decano = None
            if not os.path.exists(firma_vicerrector):
                firma_vicerrector = None

            output_file = f"certificados_generados/{fila['documento']}_{curso_nombre.replace(' ','_')}.pdf"

            # Generar certificado
            generar_certificado(
                nombre=nombre,
                documento=fila["documento"],
                curso_o_diplomado=curso_nombre,
                horas=horas,
                fecha=fecha,
                facultad=facultad,
                logo=logo,
                plantilla_fondo=plantilla_fondo,
                firma_decano=firma_decano,
                nombre_decano=nombre_decano,
                firma_vicerrector=firma_vicerrector,
                nombre_vicerrector=nombre_vicerrector,
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