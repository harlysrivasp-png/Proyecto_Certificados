import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
import os

# Crear carpeta para certificados si no existe
if not os.path.exists("certificados_generados"):
    os.makedirs("certificados_generados")

st.title("Portal de Certificados")

# Subir CSV
st.sidebar.header("Cargar archivo CSV")
uploaded_file = st.sidebar.file_uploader("Selecciona el CSV de certificados", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
        st.success("Archivo cargado correctamente")
    except Exception as e:
        st.error(f"Error al leer el CSV: {e}")
        st.stop()

    st.sidebar.header("Buscar certificado por documento")
    documento_buscar = st.sidebar.text_input("Ingrese el número de documento del estudiante:")

    if documento_buscar:
        # Asegurarse que la columna existe
        if "documento" not in df.columns:
            st.error("La columna 'documento' no existe en el CSV.")
        else:
            df["documento"] = df["documento"].astype(str)
            df_user = df[df["documento"] == documento_buscar.strip()]

            if df_user.empty:
                st.warning("No se encontraron certificados para este documento.")
            else:
                st.subheader(f"Certificados encontrados para: {documento_buscar}")

                for idx, fila in df_user.iterrows():
                    curso_nombre = fila["curso_o_diplomado"]
                    output_file = f"certificados_generados/{fila.documento}_{curso_nombre.replace(' ', '_')}.pdf"

                    generar_certificado(
                        nombre=fila.nombre,
                        documento=fila.documento,
                        curso=curso_nombre,
                        horas=fila.horas,
                        fecha=fila.fecha,
                        facultad=fila.facultad,
                        firma_decano=fila.firma_decano,
                        nombre_decano=fila.nombre_decano,
                        cargo_decano=f"{fila.cargo_decano} {fila.facultad}" if pd.notna(fila.cargo_decano) else f"Decano Facultad de {fila.facultad}",
                        firma_vicerrector=fila.firma_vicerrector,
                        nombre_vicerrector=fila.nombre_vicerrector,
                        cargo_vicerrector=fila.cargo_vicerrector if pd.notna(fila.cargo_vicerrector) else "Vicerrector Académico",
                        output_path=output_file
                    )

                    with open(output_file, "rb") as f:
                        st.download_button(
                            label=f"📄 Descargar certificado: {curso_nombre}",
                            data=f,
                            file_name=f"{fila.documento}_{curso_nombre.replace(' ','_')}.pdf",
                            mime="application/pdf"
                        )