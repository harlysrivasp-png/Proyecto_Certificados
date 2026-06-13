from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

def generar_certificado(nombre, documento, curso, horas, fecha, facultad,
                        firma_decano=None, nombre_decano="", firma_vicerrector=None,
                        nombre_vicerrector="", output_path="certificado.pdf"):
    # Crear el PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 4*cm, f"Facultad de {facultad}")

    # Cuerpo del certificado
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 6*cm, "CERTIFICA QUE")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 7*cm, nombre)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 8*cm, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(width / 2, height - 9*cm, "Participó y aprobó satisfactoriamente el curso:")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 10*cm, curso)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 11*cm, f"Con una intensidad de {horas} horas")
    c.drawCentredString(width / 2, height - 12*cm, f"Fecha de finalización: {fecha}")

    # Ajustar rutas de firmas
    if not firma_decano or not os.path.isfile(firma_decano):
        firma_decano = f"assets/firma_decano_{facultad.lower().replace(' ','')}.png"
    if not os.path.isfile(firma_decano):
        firma_decano = "assets/firma_decano_default.png"

    if not firma_vicerrector or not os.path.isfile(firma_vicerrector):
        firma_vicerrector = "assets/firma_vicerrector.png"
    if not os.path.isfile(firma_vicerrector):
        firma_vicerrector = "assets/firma_vicerrector_default.png"

    # Dibujar firmas
    firma_ancho = 4*cm
    firma_alto = 2*cm
    y_firma = 4*cm
    c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)

    # Nombres debajo de las firmas
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 1*cm, nombre_decano)
    c.drawCentredString(3*width/4, y_firma - 1*cm, nombre_vicerrector)

    c.save()
    return output_path