from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
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
    logo="assets/logo.png",
    plantilla_fondo="assets/plantilla_fondo.png",
    output_path="certificado.pdf"
):
    # Crear PDF horizontal tamaño carta
    width, height = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=(width, height))

    # Dibujar la plantilla de fondo
    if plantilla_fondo:
        c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height)

    # Logo
    if logo:
        c.drawImage(ImageReader(logo), 2*cm, height - 5*cm, width=4*cm, preserveAspectRatio=True, mask='auto')

    # Ajuste de título y subtítulo más abajo
    y_titulo = height - 4*cm
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, y_titulo, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")

    c.setFont("Helvetica", 16)
    y_subtitulo = y_titulo - 1.2*cm
    c.drawCentredString(width/2, y_subtitulo, f"Facultad de {facultad}")

    # Texto principal
    y_inicio = y_subtitulo - 3*cm
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y_inicio, "CERTIFICA QUE")

    c.setFont("Helvetica-Bold", 20)
    y_nombre = y_inicio - 1.5*cm
    c.drawCentredString(width/2, y_nombre, nombre)

    c.setFont("Helvetica", 14)
    y_doc = y_nombre - 1*cm
    c.drawCentredString(width/2, y_doc, f"Identificado(a) con documento No. {documento}")

    y_curso = y_doc - 1*cm
    c.drawCentredString(width/2, y_curso, "Participó y aprobó satisfactoriamente el curso:")
    
    y_curso_nombre = y_curso - 1*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y_curso_nombre, curso)

    y_horas = y_curso_nombre - 1*cm
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y_horas, f"Con una intensidad de {horas} horas")

    y_fecha = y_horas - 1*cm
    c.drawCentredString(width/2, y_fecha, f"Fecha de finalización: {fecha}")

    # Firmas
    y_firma = 4*cm
    firma_ancho = 6*cm
    firma_alto = 3*cm

    if firma_decano:
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    if firma_vicerrector:
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)

    # Línea y nombres debajo de la firma
    y_nombre_firma = y_firma - 0.3*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/4, y_nombre_firma, nombre_decano)
    c.drawCentredString(3*width/4, y_nombre_firma, nombre_vicerrector)

    c.setFont("Helvetica", 12)
    y_cargo_firma = y_nombre_firma - 0.5*cm
    c.drawCentredString(width/4, y_cargo_firma, f"Decano(a) Facultad de {facultad}")
    c.drawCentredString(3*width/4, y_cargo_firma, "Vicerrector Académico")

    c.save()
    return output_path