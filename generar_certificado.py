# generar_certificado.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import io
import os

def generar_certificado(nombre, documento, curso, horas, fecha, facultad,
                        firma_decano_path, nombre_decano,
                        firma_vicerrector_path, nombre_vicerrector,
                        logo_path="assets/logo_uceva.png",
                        output_path=None):
    """
    Genera un certificado PDF en memoria (BytesIO) para Streamlit.
    
    Parámetros:
    - nombre, documento, curso, horas, fecha, facultad: datos del estudiante y curso
    - firma_decano_path, nombre_decano, firma_vicerrector_path, nombre_vicerrector: firmas y nombres
    - logo_path: ruta al logo de la universidad
    - output_path: ruta para guardar el PDF (opcional)
    
    Retorna:
    - BytesIO con el PDF
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Logo
    try:
        if logo_path and os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            c.drawImage(logo, 2*cm, height - 4*cm, width=4*cm, preserveAspectRatio=True)
    except:
        pass

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 2*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 3*cm, f"Facultad de {facultad}")

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 5*cm, "CERTIFICA QUE")

    # Nombre del estudiante
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 6*cm, nombre.upper())

    # Datos adicionales
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 7*cm, f"Documento: {documento}")
    c.drawCentredString(width/2, height - 8*cm, f"Curso/Diplomado: {curso} ({horas} horas)")
    c.drawCentredString(width/2, height - 9*cm, f"Fecha: {fecha}")

    # Firmas
    y_firma = 4*cm
    if firma_decano_path and os.path.exists(firma_decano_path):
        c.drawImage(firma_decano_path, width/4 - 2*cm, y_firma, width=4*cm, preserveAspectRatio=True)
    if firma_vicerrector_path and os.path.exists(firma_vicerrector_path):
        c.drawImage(firma_vicerrector_path, 3*width/4 - 2*cm, y_firma, width=4*cm, preserveAspectRatio=True)

    # Nombres y cargos (maneja vacíos)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/4, y_firma - 1*cm, str(nombre_decano or ""))
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/4, y_firma - 1.5*cm, "Decano/a")

    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(3*width/4, y_firma - 1*cm, str(nombre_vicerrector or ""))
    c.setFont("Helvetica", 9)
    c.drawCentredString(3*width/4, y_firma - 1.5*cm, "Vicerrector/a")

    c.showPage()
    c.save()
    buffer.seek(0)

    # Guardar archivo físico si se proporciona output_path
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(buffer.getbuffer())

    return buffer