from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generar_certificado(nombre, documento, programa, horas, fecha):
    archivo = f"certificado_{documento}_{programa.replace(' ', '_')}.pdf"
    c = canvas.Canvas(archivo, pagesize=landscape(letter))
    ancho, alto = landscape(letter)

    # =========================
    # FONDO (opcional)
    # =========================
    try:
        fondo = ImageReader("assets/fondo_certificado.png")  # tu fondo
        c.drawImage(fondo, 0, 0, width=ancho, height=alto)
    except Exception:
        pass  # si no existe el fondo, se omite

    # =========================
    # LOGO
    # =========================
    try:
        logo = ImageReader("assets/logo.png")  # tu logo
        c.drawImage(logo, 50, alto - 100, width=150, height=80)  # posición y tamaño
    except Exception:
        pass  # si no existe el logo, se omite

    # =========================
    # Título
    # =========================
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(ancho / 2, alto - 100, "CERTIFICADO")

    # =========================
    # Texto principal
    # =========================
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 180, "La Institución certifica que")

    # Nombre del estudiante
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 230, str(nombre))

    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 280, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(ancho / 2, alto - 320, f"Participó y aprobó satisfactoriamente el programa:")

    # Programa
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ancho / 2, alto - 360, str(programa))

    # Horas y fecha
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 410, f"Con una intensidad de {horas} horas")
    c.drawCentredString(ancho / 2, alto - 450, f"Fecha de finalización: {fecha}")

    # =========================
    # Firmas
    # =========================
    try:
        firma1 = ImageReader("assets/firma1.png")  # firma izquierda
        c.drawImage(firma1, ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(ancho / 4 - 75, 100, ancho / 4 + 75, 100)  # línea si no hay firma
    c.drawCentredString(ancho / 4, 60, "Dirección Académica")

    try:
        firma2 = ImageReader("assets/firma2.png")  # firma derecha
        c.drawImage(firma2, 3 * ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(3 * ancho / 4 - 75, 100, 3 * ancho / 4 + 75, 100)
    c.drawCentredString(3 * ancho / 4, 60, "Coordinación Académica")

    c.save()
    return archivo