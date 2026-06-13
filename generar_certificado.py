from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

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
    logo,
    plantilla_fondo,
    output_path
):
    # Crear canvas tamaño carta horizontal
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Fondo
    c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo
    c.drawImage(ImageReader(logo), 7*cm, height - 8*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Encabezado
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 4*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 5*cm, f"Facultad de {facultad}")

    # Certificación
    y = height - 8*cm
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")
    y -= 1.2*cm
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, y, nombre)
    y -= 1*cm
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Participó y aprobó satisfactoriamente el curso:")
    y -= 0.8*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, curso_o_diplomado)
    y -= 0.8*cm
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")
    y -= 0.8*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")

    # Firmas
    y_firma = 5*cm
    firma_ancho = 6*cm
    firma_alto = 3*cm

    # Línea debajo de firmas
    c.setLineWidth(1)
    c.line(width/4 - 3*cm, y_firma - 0.5*cm, width/4 + 3*cm, y_firma - 0.5*cm)
    c.line(3*width/4 - 3*cm, y_firma - 0.5*cm, 3*width/4 + 3*cm, y_firma - 0.5*cm)

    # Imágenes de firmas
    c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto, mask='auto')
    c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto, mask='auto')

    # Nombres y cargos
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/4, y_firma - 1.2*cm, nombre_decano)
    c.drawCentredString(3*width/4, y_firma - 1.2*cm, nombre_vicerrector)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 1.6*cm, f"Decano(a) Facultad de {facultad}")
    c.drawCentredString(3*width/4, y_firma - 1.6*cm, "Vicerrector Académico")

    c.showPage()
    c.save()