# generar_certificado.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

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
    logo_path="assets/logo_uceva.png",
    plantilla_fondo="assets/fondo_certificado.png",
    output_path="certificados_generados/certificado.pdf"
):
    """
    Genera un certificado en PDF con logo, fondo, firmas, líneas y nombres.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)

    # Fondo
    if os.path.exists(plantilla_fondo):
        c.drawImage(ImageReader(plantilla_fondo), 0, 0, width=width, height=height, mask='auto')

    # Logo superior izquierdo
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), 2*cm, height - 4*cm, width=4*cm, height=3*cm, mask='auto')

    # Encabezado
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 4*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 5*cm, f"Facultad de {facultad}")

    # Cuerpo del certificado
    y_text = height - 7*cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y_text, "CERTIFICA QUE")
    y_text -= 1.5*cm

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, y_text, nombre.upper())
    y_text -= 1*cm

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y_text, f"Identificado(a) con documento No. {documento}")
    y_text -= 1*cm
    c.drawCentredString(width/2, y_text, "Participó y aprobó satisfactoriamente el curso:")
    y_text -= 1*cm

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y_text, curso_o_diplomado)
    y_text -= 1*cm

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y_text, f"Con una intensidad de {horas} horas")
    y_text -= 1*cm
    c.drawCentredString(width/2, y_text, f"Fecha de finalización: {fecha}")

    # Firmas
    y_firma = 4*cm
    firma_ancho = 6*cm
    firma_alto = 2*cm

    # Decano
    if os.path.exists(firma_decano):
        c.drawImage(ImageReader(firma_decano), width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto, mask='auto')
    c.line(width/4 - firma_ancho/2, y_firma - 0.1*cm, width/4 + firma_ancho/2, y_firma - 0.1*cm)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/4, y_firma - 0.8*cm, nombre_decano)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/4, y_firma - 1.3*cm, f"Decano(a) Facultad de {facultad}")

    # Vicerrector
    if os.path.exists(firma_vicerrector):
        c.drawImage(ImageReader(firma_vicerrector), 3*width/4 - firma_ancho/2, y_firma, width=firma_ancho, height=firma_alto, mask='auto')
    c.line(3*width/4 - firma_ancho/2, y_firma - 0.1*cm, 3*width/4 + firma_ancho/2, y_firma - 0.1*cm)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(3*width/4, y_firma - 0.8*cm, nombre_vicerrector)
    c.setFont("Helvetica", 9)
    c.drawCentredString(3*width/4, y_firma - 1.3*cm, "Vicerrector Académico")

    c.showPage()
    c.save()
    return output_path