import streamlit as st
import pandas as pd
import os
from generar_certificado import generar_certificado

# Crear carpeta de salida si no existe
os.makedirs("certificados_generados", exist_ok=True)

st.title("Portal de Certificados")

# Cargar CSV con separador ; y manejar valores vacíos
csv_path = "data/certificados_streamlit_ready.csv"
try:
    df = pd.read_csv(csv_path, sep=';', encoding="utf-8-sig").fillna("")
except Exception as e:
    st.error(f"No se pudo leer el CSV: {e}")
    st.stop()

# Convertir documento a string para evitar problemas
if "documento" not in df.columns:
    st.error("El CSV debe tener la columna 'documento'")
    st.stop()
df["documento"] = df["documento"].astype(str)

# Input de documento
documento_buscar = st.text_input("Ingrese el número de documento del estudiante:")

if documento_buscar:
    df_user = df[df["documento"].astype(str) == documento_buscar]
    if df_user.empty:
        st.warning("No se encontró ningún registro con ese documento")
    else:
        st.write(f"Se encontraron {len(df_user)} curso(s)/diplomado(s) para este estudiante.")

        # Mostrar y generar los certificados
        for idx, fila in df_user.iterrows():
            curso_nombre = fila.get("curso_o_diplomado", "Curso Desconocido")
            horas = fila.get("horas", "0")
            fecha = fila.get("fecha", "")
            facultad = fila.get("facultad", "")
            firma_decano = fila.get("firma_decano", "assets/firma_decano.png")
            nombre_decano = fila.get("nombre_decano", "")
            firma_vicerrector = fila.get("firma_vicerrector", "assets/firma_vicerrector.png")
            nombre_vicerrector = fila.get("nombre_vicerrector", "")

            output_file = f"certificados_generados/{fila['documento']}_{curso_nombre.replace(' ','_')}.pdf"

            # Generar PDF
            generar_certificado(
                nombre=fila.get("nombre", ""),
                documento=fila.get("documento", ""),
                curso_o_diplomado=curso_nombre,
                horas=horas,
                fecha=fecha,
                facultad=facultad,
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