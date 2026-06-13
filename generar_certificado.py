# generar_certificado.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def validar_firma(ruta, default):
    """
    Retorna la ruta si existe, si no retorna la ruta por defecto.
    """
    if ruta and os.path.isfile(ruta):
        return ruta
    if os.path.isfile(default):
        return default
    return None

def generar_certificado(
    nombre,
    documento,
    curso,
    horas,
    fecha,
    facultad,
    firma_decano=None,
    nombre_decano="",
    firma_vicerrector=None,
    nombre_vicerrector="",
    output_path="certificado.pdf"
):
    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)

    # --- Encabezado ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-4*cm, f"Facultad de {facultad}")

    # --- Texto principal ---
    y = height - 6*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")
    y -= 1.5*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, nombre)
    y -= 1*cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, "Participó y aprobó satisfactoriamente el curso:")
    y -= 0.8*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, curso)
    y -= 0.8*cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")

    # --- Validar firmas ---
    firma_decano = validar_firma(
        firma_decano, f"assets/firma_decano_{facultad.lower().replace(' ','')}.png"
    )
    firma_vicerrector = validar_firma(
        firma_vicerrector, "assets/firma_vicerrector.png"
    )

    # --- Firmas ---
    y_firma = 4*cm
    firma_ancho = 4*cm
    firma_alto = 2*cm

    if firma_decano:
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    if firma_vicerrector:
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)

    # Nombres debajo de las firmas
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 1*cm, nombre_decano)
    c.drawCentredString(3*width/4, y_firma - 1*cm, nombre_vicerrector)

    c.save()
    return output_path