from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
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
    logo="assets/logo.png",
    plantilla_fondo="assets/plantilla_fondo.png",
    output_path="certificado.pdf"
):
    # Configuración de la página en horizontal (landscape)
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Imagen de fondo (tamaño completo)
    c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo UCEVA
    c.drawImage(ImageReader(logo), 3*cm, height - 20*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Título principal
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 4*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")

    # Subtítulo: Facultad
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 5*cm, f"Facultad de {facultad}")

    # Texto central
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 7*cm, "CERTIFICA QUE")

    c.setFont("Helvetica-Bold", 23)
    c.drawCentredString(width/2, height - 9*cm, nombre)

    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 10*cm, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(width/2, height - 11*cm, "Participó y aprobó satisfactoriamente el curso:")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 13*cm, f"{curso_o_diplomado}")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 14*cm, f"Con una intensidad de {horas} horas")
    c.drawCentredString(width/2, height - 15*cm, f"Fecha de finalización: {fecha}")

    # Posición de las firmas
    y_firma = 3*cm
    firma_ancho = 6*cm
    firma_alto = 3*cm

    # Firma del decano
    c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma + 0.7*cm, width=firma_ancho, height=firma_alto, preserveAspectRatio=True, mask='auto')
    # Línea horizontal bajo la firma
    c.line(width/4 - firma_ancho/2, y_firma + 0.5*cm, width/4 + firma_ancho/2, y_firma + 0.5*cm)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/4, y_firma, nombre_decano)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 0.5*cm, f"Decano(a) Facultad de {facultad}")

    # Firma del vicerrector
    c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma + 0.7*cm, width=firma_ancho, height=firma_alto, preserveAspectRatio=True, mask='auto')
    # Línea horizontal bajo la firma
    c.line(3*width/4 - firma_ancho/2, y_firma + 0.5*cm, 3*width/4 + firma_ancho/2, y_firma + 0.5*cm)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(3*width/4, y_firma, nombre_vicerrector)
    c.setFont("Helvetica", 10)
    c.drawCentredString(3*width/4, y_firma - 0.5*cm, "Vicerrector Académico")

    c.showPage()
    c.save()