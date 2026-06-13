import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado
from io import BytesIO

st.set_page_config(page_title="Portal de Certificados", layout="wide")
st.title("📄 Portal de Certificados - UCEVA")

# Cargar datos de certificados
df = pd.read_csv("certificados.csv")  # Asegúrate que tenga columnas: nombre, documento, programa, horas, fecha, logo, firma_decano, cargo_decano, firma_vicerrector, cargo_vicerrector

# Selección de documento
documento = st.text_input("Ingrese el número de documento del estudiante:")

if documento:
    estudiante = df[df["documento"] == int(documento)]
    
    if estudiante.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"Se encontraron {len(estudiante)} certificado(s) para este estudiante.")
        
        cols = st.columns(len(estudiante))  # Botones en horizontal
        
        for i, (index, fila) in enumerate(estudiante.iterrows()):
            with cols[i]:
                archivo_pdf = generar_certificado(
                    nombre=fila["nombre"],
                    documento=fila["documento"],
                    programa=fila["programa"],
                    horas=fila["horas"],
                    fecha=fila["fecha"],
                    logo_path=fila.get("logo", "assets/logo_default.png"),
                    firma1=fila.get("firma_decano", "assets/decano_default.png"),
                    cargo1=fila.get("cargo_decano", "Decano/a"),
                    firma2=fila.get("firma_vicerrector", "assets/vicerrector_default.png"),
                    cargo2=fila.get("cargo_vicerrector", "Vicerrector/a")
                )

                st.download_button(
                    label=f"📄 Descargar: {fila['programa']}",
                    data=archivo_pdf,
                    file_name=f"certificado_{fila['documento']}_{fila['programa']}.pdf",
                    mime="application/pdf"
                )