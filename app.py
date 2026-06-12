import streamlit as st
import pandas as pd
from generar_certificado import generar_certificado

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Portal de Certificados",
    page_icon="🎓",
    layout="centered"
)

# ==========================================
# ENCABEZADO
# ==========================================
st.title("🎓 Portal de Certificados - Oficina de Educación Virtual y a Distancia - UCEVA")
st.write("Consulta y descarga tus certificados académicos")

# ==========================================
# CARGAR BASE DE DATOS
# ==========================================
try:
    df = pd.read_csv("data/certificados.csv", encoding="latin1", sep=";")
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error al leer el archivo CSV: {e}")
    st.stop()

# ==========================================
# INGRESAR DOCUMENTO
# ==========================================
documento = st.text_input("Ingrese su número de documento")

# ==========================================
# BOTÓN BUSCAR
# ==========================================
if st.button("Buscar Certificado"):

    resultado = df[df["documento"].astype(str).str.strip() == documento.strip()]

    if resultado.empty:
        st.warning("No se encontraron certificados para este documento.")
    else:
        st.success(f"{len(resultado)} certificado(s) encontrado(s)")

        # Crear columnas para botones horizontales
        columnas = st.columns(len(resultado))

        for i, fila in enumerate(resultado.itertuples()):
            # Generar PDF con firmas dinámicas
            archivo_pdf = generar_certificado(
                fila.nombre,
                fila.documento,
                fila.programa,
                getattr(fila, "horas", ""),
                getattr(fila, "fecha", ""),
                getattr(fila, "firma_decano", "assets/decano_default.png"),
                getattr(fila, "firma_vicerrector", "assets/vicerrector_default.png")
            )

            # Mostrar cada botón en su columna
            with columnas[i]:
                st.subheader(f"Certificado {i+1}")
                st.write(f"**Nombre:** {fila.nombre}")
                st.write(f"**Programa:** {fila.programa}")
                if hasattr(fila, "horas"):
                    st.write(f"**Horas:** {fila.horas}")
                if hasattr(fila, "fecha"):
                    st.write(f"**Fecha:** {fila.fecha}")

                st.download_button(
                    label="📄 Descargar Certificado",
                    data=open(archivo_pdf, "rb").read(),
                    file_name=archivo_pdf,
                    mime="application/pdf",
                    key=f"download_{i}"
                )