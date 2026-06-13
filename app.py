import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

# Título de la app
st.title("Portal de Certificados")

# Crear carpeta para guardar certificados generados
os.makedirs("certificados_generados", exist_ok=True)

# Cargar CSV
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Input de documento
documento_buscar = st.text_input("Ingrese el documento del estudiante")

if documento_buscar:
    # Filtrar por documento
    df["documento"] = df["documento"].astype(str)
    df_user = df[df["documento"] == documento_buscar]

    if df_user.empty:
        st.warning("No se encontraron certificados para ese documento.")
    else:
        st.write(f"Se encontraron {len(df_user)} certificados para el documento {documento_buscar}.")

        for idx, fila in df_user.iterrows():
            curso_nombre = fila["curso_o_diplomado"]
            output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ','_')}.pdf"

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
                output_path=output_file
            )

            st.success(f"Certificado generado para {curso_nombre}")

            # Botón de descarga
            with open(output_file, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label=f"📄 Descargar {curso_nombre}",
                    data=pdf_bytes,
                    file_name=os.path.basename(output_file),
                    mime="application/pdf"
                )