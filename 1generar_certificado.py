from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


def generar_certificado(nombre, documento, programa, horas, fecha):

    archivo = f"certificado_{documento}.pdf"

    c = canvas.Canvas(
        archivo,
        pagesize=landscape(letter)
    )

    ancho, alto = landscape(letter)

    # Título
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(
        ancho / 2,
        alto - 100,
        "CERTIFICADO"
    )

    # Texto principal
    c.setFont("Helvetica", 16)

    c.drawCentredString(
        ancho / 2,
        alto - 180,
        "La Institución certifica que"
    )

    # Nombre
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        ancho / 2,
        alto - 230,
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

    # Firma
    c.line(
        ancho / 2 - 100,
        120,
        ancho / 2 + 100,
        120
    )

    c.drawCentredString(
        ancho / 2,
        100,
        "Dirección Académica"
    )

    c.save()

    return archivo