from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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
    cargo_decano,
    firma_vicerrector,
    nombre_vicerrector,
    cargo_vicerrector,
    output_path
):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 4*cm, f"Facultad de {facultad}")

    # Cuerpo
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 6*cm, "CERTIFICA QUE")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 7*cm, nombre)

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 8*cm, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(width/2, height - 9*cm, f"Participó y aprobó satisfactoriamente el curso:")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 10*cm, f"{curso}")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 11*cm, f"Con una intensidad de {horas} horas")
    c.drawCentredString(width/2, height - 12*cm, f"Fecha de finalización: {fecha}")

    # Firmas
    firma_ancho = 5*cm
    firma_alto = 2*cm
    y_firma = 3*cm

    # Línea debajo de la firma
    c.line(width/4 - firma_ancho/2, y_firma, width/4 + firma_ancho/2, y_firma)
    c.line(3*width/4 - firma_ancho/2, y_firma, 3*width/4 + firma_ancho/2, y_firma)

    # Dibujar imágenes de firma
    try:
        if firma_decano:
            c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
        if firma_vicerrector:
            c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto)
    except Exception as e:
        print(f"No se pudo cargar la firma: {e}")

    # Nombres y cargos
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 0.7*cm, str(nombre_decano))
    c.drawCentredString(width/4, y_firma - 1.2*cm, str(cargo_decano))

    c.drawCentredString(3*width/4, y_firma - 0.7*cm, str(nombre_vicerrector))
    c.drawCentredString(3*width/4, y_firma - 1.2*cm, str(cargo_vicerrector))

    c.save()