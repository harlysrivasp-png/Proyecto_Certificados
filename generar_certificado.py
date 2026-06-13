from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def generar_certificado(nombre, documento, curso, horas, fecha, facultad,
                        firma_decano, nombre_decano,
                        firma_vicerrector, nombre_vicerrector,
                        output_path="certificado.pdf"):

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Crear PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # --- Encabezado ---
    # Logo UCEVA (si existe)
    logo_path = "assets/logo_uceva.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 2*cm, height - 3*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Título central
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 2*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")

    # Subtítulo: Facultad dinámica
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 3*cm, f"Facultad de {facultad}")

    # --- Contenido ---
    y = height - 5*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")

    y -= 1.5*cm
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, nombre.upper())

    y -= 1*cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")

    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Participó y aprobó satisfactoriamente el curso:")

    y -= 0.8*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, f"{curso}")

    y -= 0.8*cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")

    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")

    # --- Firmas ---
    y_firma = 3*cm
    firma_width = 5*cm
    firma_height = 2*cm

    # Firma decano
    if os.path.exists(firma_decano):
        c.drawImage(firma_decano, width/4 - firma_width/2, y_firma, width=firma_width, height=firma_height, mask='auto')
    c.drawCentredString(width/4, y_firma - 0.5*cm, nombre_decano)
    c.drawCentredString(width/4, y_firma - 1*cm, "Decano")

    # Firma vicerrector
    if os.path.exists(firma_vicerrector):
        c.drawImage(firma_vicerrector, 3*width/4 - firma_width/2, y_firma, width=firma_width, height=firma_height, mask='auto')
    c.drawCentredString(3*width/4, y_firma - 0.5*cm, nombre_vicerrector)
    c.drawCentredString(3*width/4, y_firma - 1*cm, "Vicerrector Académico")

    # Guardar PDF
    c.save()
    return output_path