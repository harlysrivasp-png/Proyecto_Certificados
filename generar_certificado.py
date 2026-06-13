# generar_certificado.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def generar_certificado(
    nombre,
    documento,
    curso,
    horas,
    fecha,
    facultad,
    firma_decano,
    nombre_decano,
    firma_vicerrector,
    nombre_vicerrector,
    logo_uceva="assets/logo_uceva.png",
    plantilla_fondo="assets/plantilla_fondo.png",
    output_path="certificado.pdf"
):
    """
    Genera un certificado PDF con logo, fondo y firmas.
    """
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Plantilla de fondo
    if plantilla_fondo and os.path.exists(plantilla_fondo):
        c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo en la esquina superior izquierda
    if logo_uceva and os.path.exists(logo_uceva):
        c.drawImage(ImageReader(logo_uceva), 2*cm, height - 4*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Encabezado
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 4*cm, f"Facultad de {facultad}")

    # Certificación
    y = height - 7*cm
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")
    y -= 1*cm

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, y, nombre)
    y -= 0.8*cm

    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, "Participó y aprobó satisfactoriamente el curso:")
    y -= 0.8*cm

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, curso)
    y -= 0.8*cm

    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")
    y -= 2*cm

    # Firmas
    firma_ancho = 6*cm
    firma_alto = 3*cm
    y_firma = y

    # Decano
    if os.path.exists(firma_decano):
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.line(width/4 - firma_ancho/2, y_firma - 2, width/4 + firma_ancho/2, y_firma - 2)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/4, y_firma - 0.7*cm, nombre_decano)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/4, y_firma - 1.2*cm, f"Decano(a) Facultad de {facultad}")

    # Vicerrector
    if os.path.exists(firma_vicerrector):
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.line(3*width/4 - firma_ancho/2, y_firma - 2, 3*width/4 + firma_ancho/2, y_firma - 2)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(3*width/4, y_firma - 0.7*cm, nombre_vicerrector)
    c.setFont("Helvetica", 11)
    c.drawCentredString(3*width/4, y_firma - 1.2*cm, "Vicerrector Académico")

    # Guardar PDF
    c.save()