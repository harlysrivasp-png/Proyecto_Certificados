from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

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
    output_path
):
    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-4*cm, f"Facultad de {facultad}")

    # Certifica que
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-6*cm, "CERTIFICA QUE")

    # Nombre
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-7*cm, nombre)

    # Documento
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-8*cm, f"Identificado(a) con documento No. {documento}")

    # Curso
    c.drawCentredString(width/2, height-9*cm, "Participó y aprobó satisfactoriamente el curso:")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-10*cm, f"{curso} ({horas} horas)")

    # Fecha
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-11*cm, f"Fecha de finalización: {fecha}")

    # Firmas
    y_firma = 4*cm
    firma_ancho = 5*cm
    firma_alto = 2*cm

    # Firma decano
    if firma_decano:
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.drawCentredString(width/4, y_firma - 0.5*cm, nombre_decano)
    c.drawCentredString(width/4, y_firma - 1*cm, "Decano(a) Facultad")

    # Firma vicerrector
    if firma_vicerrector:
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    c.drawCentredString(3*width/4, y_firma - 0.5*cm, nombre_vicerrector)
    c.drawCentredString(3*width/4, y_firma - 1*cm, "Vicerrector(a)")

    c.save()
    return output_path