# generar_certificado.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

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
    logo_uc,
    output_path
):
    """Genera un certificado en PDF con datos y firmas dinámicas."""
    
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Logo UCEVA
    if os.path.exists(logo_uc):
        logo = ImageReader(logo_uc)
        c.drawImage(logo, 3*cm, height - 4*cm, width=4*cm, preserveAspectRatio=True, mask='auto')
    
    # Título principal
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 3*cm, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")
    
    # Subtítulo facultad
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 4*cm, f"Facultad de {facultad}")
    
    # Texto Certifica que
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 6*cm, "CERTIFICA QUE")
    
    # Nombre estudiante
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 7*cm, nombre.upper())
    
    # Información adicional
    c.setFont("Helvetica", 12)
    y_texto = height - 8*cm
    c.drawCentredString(width/2, y_texto, f"Identificado(a) con documento No. {documento}")
    c.drawCentredString(width/2, y_texto - 0.6*cm, "Participó y aprobó satisfactoriamente el curso:")
    c.drawCentredString(width/2, y_texto - 1.2*cm, curso.upper())
    c.drawCentredString(width/2, y_texto - 1.8*cm, f"Con una intensidad de {horas} horas")
    c.drawCentredString(width/2, y_texto - 2.4*cm, f"Fecha de finalización: {fecha}")
    
    # Firmas
    y_firma = 5*cm
    if os.path.exists(firma_decano):
        decano_img = ImageReader(firma_decano)
        c.drawImage(decano_img, width/4 - 3*cm, y_firma, width=4*cm, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/4, y_firma - 1*cm, nombre_decano)
    c.drawCentredString(width/4, y_firma - 1.5*cm, "Decano Facultad")
    
    if os.path.exists(firma_vicerrector):
        vic_img = ImageReader(firma_vicerrector)
        c.drawImage(vic_img, 3*width/4 - 3*cm, y_firma, width=4*cm, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica", 10)
    c.drawCentredString(3*width/4, y_firma - 1*cm, nombre_vicerrector)
    c.drawCentredString(3*width/4, y_firma - 1.5*cm, "Vicerrector Académico")
    
    c.showPage()
    c.save()
    
    return output_path