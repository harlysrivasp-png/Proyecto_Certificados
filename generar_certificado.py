from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os


def generar_certificado(nombre, documento, programa, horas, fecha):

    # ==========================================
    # RUTAS
    # ==========================================

    carpeta_salida = "certificados_generados"
    os.makedirs(carpeta_salida, exist_ok=True)

    archivo = os.path.join(
        carpeta_salida,
        f"certificado_{documento}.pdf"
    )

    fondo = "assets/fondo_certificado.png"
    logo = "assets/logo.png"
    firma_1 = "assets/firma_1.png"
    firma_2 = "assets/firma_2.png"

    # ==========================================
    # CREAR PDF
    # ==========================================

    c = canvas.Canvas(
        archivo,
        pagesize=landscape(letter)
    )

    ancho, alto = landscape(letter)

    # ==========================================
    # FONDO
    # ==========================================

    if os.path.exists(fondo):
        c.drawImage(
            ImageReader(fondo),
            0,
            0,
            width=ancho,
            height=alto,
            preserveAspectRatio=False,
            mask="auto"
        )

    # ==========================================
    # LOGO
    # ==========================================

    if os.path.exists(logo):
        c.drawImage(
            ImageReader(logo),
            60,
            alto - 105,
            width=130,
            height=55,
            preserveAspectRatio=True,
            mask="auto"
        )

    # ==========================================
    # ENCABEZADO
    # ==========================================

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(
        ancho / 2+6,
        alto - 125,
        "UNIDAD CENTRAL DEL VALLE DEL CAUCA"
    )

    c.setFont("Helvetica", 15)
    c.drawCentredString(
        ancho / 2 + 5,
        alto - 150,
        "Oficina de Educación Virtual y a Distancia"
    )

    # ==========================================
    # TÍTULO
    # ==========================================

    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(
        ancho / 2,
        alto - 209,
        "CERTIFICA QUE"
    )

    # ==========================================
    # TEXTO PRINCIPAL
    # ==========================================

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        ancho / 2,
        alto - 230,
        "El/la participante"
    )

    # Nombre
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        ancho / 2,
        alto - 275,
        str(nombre).upper()
    )

    c.setFont("Helvetica", 15)
    c.drawCentredString(
        ancho / 2,
        alto - 305,
        f"Identificado(a) con documento No. {documento}"
    )

    c.drawCentredString(
        ancho / 2,
        alto - 335,
        "Participó y aprobó satisfactoriamente el curso:"
    )

    # Programa
    c.setFont("Helvetica-Bold", 19)
    c.drawCentredString(
        ancho / 2,
        alto - 375,
        str(programa).upper()
    )

    c.setFont("Helvetica", 15)
    c.drawCentredString(
        ancho / 2,
        alto - 420,
        f"Con una intensidad de {horas} horas"
    )

    c.drawCentredString(
        ancho / 2,
        alto - 455,
        f"Fecha de finalización: {fecha}"
    )

    # ==========================================
    # FIRMAS
    # ==========================================

    # Firma izquierda
    if os.path.exists(firma_1):
        c.drawImage(
            ImageReader(firma_1),
            140,
            90,
            width=160,
            height=70,
            preserveAspectRatio=True,
            mask="auto"
        )

    c.line(
        130,
        105,
        350,
        105
    )

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(
        240,
        85,
        "Gustavo Cárdenas"
    )

    c.setFont("Helvetica", 10)
    c.drawCentredString(
        240,
        70,
        "Vicerrector Académico"
    )

    # Firma derecha
    if os.path.exists(firma_2):
        c.drawImage(
            ImageReader(firma_2),
            ancho - 300,
            90,
            width=160,
            height=70,
            preserveAspectRatio=True,
            mask="auto"
        )

    c.line(
        ancho - 350,
        105,
        ancho - 130,
        105
    )

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(
        ancho - 240,
        85,
        "Juan Albero Pérez"
    )

    c.setFont("Helvetica", 10)
    c.drawCentredString(
        ancho - 240,
        70,
        "Decano Facultad"
    )

    # ==========================================
    # GUARDAR PDF
    # ==========================================

    c.save()

    return archivo