# generar_certificado.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def generar_certificado(
    nombre,
    documento,
    curso_o_diplomado,
    horas,
    fecha,
    facultad,
    logo=None,
    plantilla_fondo=None,
    firma_decano=None,
    nombre_decano="",
    firma_vicerrector=None,
    nombre_vicerrector="",
    output_path="certificado.pdf"
):
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Fondo
    if plantilla_fondo and os.path.exists(plantilla_fondo):
        c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo
    if logo and os.path.exists(logo):
        c.drawImage(ImageReader(logo), 2*cm, height - 5*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Título y subtítulo
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 4*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 5*cm, f"Facultad de {facultad}")

    # Cuerpo
    y = height - 7*cm
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")
    y -= 1.5*cm

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, y, nombre)
    y -= 1*cm

    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, "Participó y aprobó satisfactoriamente el curso:")
    y -= 0.8*cm

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, curso_o_diplomado)
    y -= 0.8*cm

    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")

    # Firmas
    firma_ancho = 6*cm
    firma_alto = 3*cm
    y_firma = 3*cm

    if firma_decano and os.path.exists(firma_decano):
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/4, y_firma - 0.5*cm, nombre_decano)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 1*cm, f"Decano(a) Facultad de {facultad}")

    if firma_vicerrector and os.path.exists(firma_vicerrector):
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(3*width/4, y_firma - 0.5*cm, nombre_vicerrector)
    c.setFont("Helvetica", 10)
    c.drawCentredString(3*width/4, y_firma - 1*cm, "Vicerrector Académico")

    c.showPage()
    c.save()
    return output_path