import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# --- Configuración de la página ---
st.set_page_config(page_title="Portal de Certificados", layout="wide")

# --- Título ---
st.title("Portal de Certificados")
st.write("Ingrese su documento para consultar y descargar sus certificados")

# --- Leer CSV ---
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, encoding="utf-8")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

# Limpiar nombres de columnas (eliminar espacios)
df.columns = df.columns.str.strip()

# Convertir documento a string
df["documento"] = df["documento"].astype(str)

# --- Entrada del usuario ---
documento_buscar = st.text_input("Documento:")

if documento_buscar:
    df_user = df[df["documento"] == documento_buscar]
    
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(df_user)} certificado(s).")

        # Contenedor horizontal para botones
        cols = st.columns(len(df_user))

        for i, (index, fila) in enumerate(df_user.iterrows()):
            curso_nombre = fila["curso o diplomado"]
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ', '_')}.pdf"

            # Generar certificado
            generar_certificado(
                nombre=fila["nombre"],
                documento=fila["documento"],
                curso=curso_nombre,
                horas=fila["horas"],
                fecha=fila["fecha"],
                facultad=fila["facultad"],
                firma_decano=fila.get("firma_decano", "assets/decano_default.png"),
                nombre_decano=fila.get("nombre_decano", ""),
                firma_vicerrector=fila.get("firma_vicerrector", "assets/vicerrector_default.png"),
                nombre_vicerrector=fila.get("nombre_vicerrector", ""),
                output_path=output_file
            )

            # Botón de descarga
            with cols[i]:
                with open(output_file, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    st.download_button(
                        label=f"📄 {curso_nombre}",
                        data=pdf_bytes,
                        file_name=os.path.basename(output_file),
                        mime="application/pdf"
                    )