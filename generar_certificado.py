# generar_certificado.py

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
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
    firma_decano,
    nombre_decano,
    firma_vicerrector,
    nombre_vicerrector,
    output_path,
    logo_uceva="assets/logo_uceva.png",
    plantilla_fondo=None
):
    """
    Genera un certificado PDF con firma y logo.
    """
    # Crear canvas tamaño carta horizontal
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Si existe plantilla de fondo, dibujarla
    if plantilla_fondo and os.path.exists(plantilla_fondo):
        c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo UCEVA en la esquina superior izquierda
    if os.path.exists(logo_uceva):
        c.drawImage(ImageReader(logo_uceva), 2*cm, height - 5*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Título principal
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 4*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")

    # Subtítulo Facultad
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 5*cm, f"Facultad de {facultad}")

    # Texto certificado
    y_texto = height - 8*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y_texto, "CERTIFICA QUE")
    y_texto -= 1*cm

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y_texto, nombre)
    y_texto -= 0.8*cm

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y_texto, f"Identificado(a) con documento No. {documento}")
    y_texto -= 0.8*cm

    c.drawCentredString(width/2, y_texto, f"Participó y aprobó satisfactoriamente el curso:")
    y_texto -= 0.8*cm

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y_texto, f"{curso_o_diplomado}")
    y_texto -= 0.8*cm

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y_texto, f"Con una intensidad de {horas} horas")
    y_texto -= 0.8*cm

    c.drawCentredString(width/2, y_texto, f"Fecha de finalización: {fecha}")
    y_texto -= 2*cm

    # Firmas
    firma_ancho = 6*cm
    firma_alto = 3*cm
    y_firma = y_texto

    # Firma decano
    if os.path.exists(firma_decano):
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    # Línea bajo firma
    c.line(width/4 - firma_ancho/2, y_firma - 2, width/4 + firma_ancho/2, y_firma - 2)
    # Nombre y cargo
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 0.5*cm - firma_alto, nombre_decano)
    c.drawCentredString(width/4, y_firma - 1*cm - firma_alto, f"Decano(a) Facultad de {facultad}")

    # Firma vicerrector
    if os.path.exists(firma_vicerrector):
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    # Línea bajo firma
    c.line(3*width/4 - firma_ancho/2, y_firma - 2, 3*width/4 + firma_ancho/2, y_firma - 2)
    # Nombre y cargo
    c.setFont("Helvetica", 10)
    c.drawCentredString(3*width/4, y_firma - 0.5*cm - firma_alto, nombre_vicerrector)
    c.drawCentredString(3*width/4, y_firma - 1*cm - firma_alto, "Vicerrector Académico")

    # Guardar PDF
    c.save()