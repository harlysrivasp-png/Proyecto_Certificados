import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado

st.set_page_config(page_title="Portal de Certificados", layout="wide")

# Cargar CSV
try:
    df = pd.read_csv("data/certificados_final_utf8.csv")
except Exception as e:
    st.error(f"Error al leer el CSV: {e}")
    st.stop()

st.title("Portal de Certificados")

# Selección de documento
documento_buscar = st.text_input("Ingrese su número de documento")

if documento_buscar:
    df_user = df[df["documento"].astype(str) == documento_buscar]
    if df_user.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.subheader(f"Certificados de {df_user.iloc[0]['nombre']}")
        # Botones horizontales
        cols = st.columns(len(df_user))
        for i, (index, fila) in enumerate(df_user.iterrows()):
            with cols[i]:
                st.write(f"{fila['programa']} - {fila['facultad']}")
                archivo_pdf = generar_certificado(
                    nombre=fila.nombre,
                    documento=fila.documento,
                    programa=fila.programa,
                    horas=fila.horas,
                    fecha=fila.fecha,
                    facultad=fila.facultad,
                    firma_decano=fila.firma_decano,
                    cargo_decano=fila.cargo_decano,
                    firma_vicerrector=fila.firma_vicerrector,
                    cargo_vicerrector=fila.cargo_vicerrector,
                    logo=fila.logo if 'logo' in fila else None
                )
                st.download_button(
                    label="📄 Descargar Certificado",
                    data=archivo_pdf,
                    file_name=f"{fila.documento}_{fila.programa}.pdf",
                    mime="application/pdf"
                )