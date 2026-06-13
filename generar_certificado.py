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
    firma_vicerrector,
    nombre_vicerrector,
    output_path
):
    """
    Genera un certificado en PDF para un estudiante con las firmas y cargos correspondientes.
    """

    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)

    # Margen superior
    y = height - 4*cm

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    y -= 0.8*cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Facultad de {facultad}")
    y -= 2*cm

    # Certifica que
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, "CERTIFICA QUE")
    y -= 1*cm

    # Nombre estudiante
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, nombre)
    y -= 1*cm

    # Documento
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Identificado(a) con documento No. {documento}")
    y -= 0.7*cm

    # Texto del curso
    c.drawCentredString(width/2, y, "Participó y aprobó satisfactoriamente el curso:")
    y -= 0.7*cm

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, curso)
    y -= 1*cm

    # Horas y fecha
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, f"Con una intensidad de {horas} horas")
    y -= 0.7*cm
    c.drawCentredString(width/2, y, f"Fecha de finalización: {fecha}")
    y -= 3*cm

    # Firmas
    firma_ancho = 5*cm
    firma_alto = 2*cm
    y_firma = y

    try:
        # Firma decano
        if firma_decano and nombre_decano:
            c.drawImage(
                ImageReader(firma_decano),
                width/4 - firma_ancho/2,
                y_firma,
                width=firma_ancho,
                height=firma_alto
            )
            c.drawCentredString(width/4, y_firma - 0.5*cm, f"{nombre_decano}")
            c.drawCentredString(width/4, y_firma - 1*cm, f"Decano(a) Facultad de {facultad}")

        # Firma vicerrector
        if firma_vicerrector and nombre_vicerrector:
            c.drawImage(
                ImageReader(firma_vicerrector),
                3*width/4 - firma_ancho/2,
                y_firma,
                width=firma_ancho,
                height=firma_alto
            )
            c.drawCentredString(3*width/4, y_firma - 0.5*cm, f"{nombre_vicerrector}")
            c.drawCentredString(3*width/4, y_firma - 1*cm, "Vicerrector Académico")
    except Exception as e:
        print(f"No se pudieron cargar las firmas: {e}")

    c.showPage()
    c.save()