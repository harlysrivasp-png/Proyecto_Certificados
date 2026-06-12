from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generar_certificado(nombre, documento, programa, horas, fecha, firma_decano, firma_vicerrector):
    archivo = f"certificado_{documento}_{programa.replace(' ', '_')}.pdf"
    c = canvas.Canvas(archivo, pagesize=landscape(letter))
    ancho, alto = landscape(letter)

    # =========================
    # FONDO
    # =========================
    try:
        fondo = ImageReader("assets/fondo_certificado.png")  # ruta del fondo
        c.drawImage(fondo, 0, 0, width=ancho, height=alto)
    except Exception:
        pass  # si no hay fondo, se omite

    # =========================
    # LOGO
    # =========================
    try:
        logo = ImageReader("assets/logo.png")
        c.drawImage(logo, 50, alto - 100, width=150, height=80)
    except Exception:
        pass

    # =========================
    # TÍTULO Y DATOS
    # =========================
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(ancho / 2, alto - 100, "CERTIFICADO")

    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 180, "La Institución certifica que")

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 230, str(nombre))

    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 280, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(ancho / 2, alto - 320, f"Participó y aprobó satisfactoriamente el programa:")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ancho / 2, alto - 360, str(programa))

    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 410, f"Con una intensidad de {horas} horas")
    c.drawCentredString(ancho / 2, alto - 450, f"Fecha de finalización: {fecha}")

    # =========================
    # FIRMAS DINÁMICAS
    # =========================
    try:
        decano = ImageReader(firma_decano)
        c.drawImage(decano, ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(ancho / 4 - 75, 100, ancho / 4 + 75, 100)
    c.drawCentredString(ancho / 4, 60, "Decano")

    try:
        vicerrector = ImageReader(firma_vicerrector)
        c.drawImage(vicerrector, 3 * ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(3 * ancho / 4 - 75, 100, 3 * ancho / 4 + 75, 100)
    c.drawCentredString(3 * ancho / 4, 60, "Vicerrector")

    c.save()
    return archivo