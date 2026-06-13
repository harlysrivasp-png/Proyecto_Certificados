from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generar_certificado(nombre, documento, programa, horas, fecha, logo_path, firma1, cargo1, firma2, cargo2):
    archivo = f"certificado_{documento}.pdf"

    c = canvas.Canvas(
        archivo,
        pagesize=landscape(letter)
    )

    ancho, alto = landscape(letter)

    # Logo en la esquina superior izquierda
    if logo_path:
        logo = ImageReader(logo_path)
        c.drawImage(logo, 50, alto - 120, width=150, height=80, preserveAspectRatio=True)

    # Encabezado principal
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        ancho / 2,
        alto - 80,
        "UNIDAD CENTRAL DEL VALLE DEL CAUCA"
    )

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        ancho / 2,
        alto - 110,
        "Oficina de Educación Virtual y a Distancia"
    )

    # Título
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(
        ancho / 2,
        alto - 180,
        "CERTIFICA QUE"
    )

    # Nombre del estudiante
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        ancho / 2,
        alto - 240,
        str(nombre)
    )

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        ancho / 2,
        alto - 280,
        f"Identificado(a) con documento No. {documento}"
    )

    c.drawCentredString(
        ancho / 2,
        alto - 320,
        f"Participó y aprobó satisfactoriamente el programa:"
    )

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(
        ancho / 2,
        alto - 360,
        str(programa)
    )

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        ancho / 2,
        alto - 410,
        f"Con una intensidad de {horas} horas"
    )

    c.drawCentredString(
        ancho / 2,
        alto - 450,
        f"Fecha de finalización: {fecha}"
    )

    # Firmas dinámicas
    if firma1:
        c.line(ancho / 4 - 100, 120, ancho / 4 + 100, 120)
        c.drawCentredString(ancho / 4, 100, str(firma1))
        c.drawCentredString(ancho / 4, 85, str(cargo1))

    if firma2:
        c.line(ancho * 3/4 - 100, 120, ancho * 3/4 + 100, 120)
        c.drawCentredString(ancho * 3/4, 100, str(firma2))
        c.drawCentredString(ancho * 3/4, 85, str(cargo2))

    c.save()
    return archivo