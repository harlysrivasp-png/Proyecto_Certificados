# generar_certificado.py
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generar_certificado(nombre, documento, programa, horas, fecha,
                        logo="assets/logo_default.png",
                        firma_decano="assets/firma_decano_default.png",
                        cargo_decano="Decano/a",
                        firma_vicerrector="assets/firma_vicerrector_default.png",
                        cargo_vicerrector="Vicerrector/a"):
    
    archivo = f"certificado_{documento}_{programa.replace(' ', '_')}.pdf"
    c = canvas.Canvas(archivo, pagesize=landscape(letter))
    ancho, alto = landscape(letter)

    # =========================
    # LOGO UCEVA
    # =========================
    try:
        logo_img = ImageReader(logo)
        c.drawImage(logo_img, 50, alto - 120, width=150, height=80, preserveAspectRatio=True)
    except Exception:
        pass

    # =========================
    # ENCABEZADO UCEVA
    # =========================
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 80, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 110, "Oficina de Educación Virtual y a Distancia")

    # =========================
    # TÍTULO CERTIFICADO
    # =========================
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(ancho / 2, alto - 180, "CERTIFICA QUE")

    # =========================
    # DATOS DEL ESTUDIANTE
    # =========================
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 240, nombre)
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 280, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(ancho / 2, alto - 320, f"Participó y aprobó satisfactoriamente el programa:")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(ancho / 2, alto - 360, programa)
    c.setFont("Helvetica", 16)
    c.drawCentredString(ancho / 2, alto - 410, f"Con una intensidad de {horas} horas")
    c.drawCentredString(ancho / 2, alto - 450, f"Fecha de finalización: {fecha}")

    # =========================
    # FIRMAS DINÁMICAS
    # =========================
    # Firma decano
    try:
        firma_decano_img = ImageReader(firma_decano)
        c.drawImage(firma_decano_img, ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(ancho / 4 - 75, 100, ancho / 4 + 75, 100)
    c.drawCentredString(ancho / 4, 60, cargo_decano)

    # Firma vicerrector
    try:
        firma_vicerrector_img = ImageReader(firma_vicerrector)
        c.drawImage(firma_vicerrector_img, 3 * ancho / 4 - 75, 80, width=150, height=50)
    except Exception:
        c.line(3 * ancho / 4 - 75, 100, 3 * ancho / 4 + 75, 100)
    c.drawCentredString(3 * ancho / 4, 60, cargo_vicerrector)

    c.save()
    return archivo