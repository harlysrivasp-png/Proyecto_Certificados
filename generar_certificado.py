from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

def generar_certificado(nombre, documento, programa, horas, fecha, facultad,
                        firma_decano, cargo_decano, firma_vicerrector, cargo_vicerrector,
                        logo=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Logo
    if logo:
        try:
            c.drawImage(logo, 50, height - 100, width=100, preserveAspectRatio=True, mask='auto')
        except:
            pass

    # Título
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "UNIDAD CENTRAL DEL VALLE DEL CAUCA")

    # Subtítulo dinámico: facultad
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 100, f"Facultad de {facultad}")

    # Certifica que
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 160, "CERTIFICA QUE")

    # Nombre
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 200, nombre)

    # Documento y curso
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 240, f"Documento: {documento}")
    c.drawCentredString(width / 2, height - 270, f"Curso: {programa} ({horas} horas)")
    c.drawCentredString(width / 2, height - 300, f"Fecha: {fecha}")

    # Firmas
    firma_y = 100
    c.drawImage(firma_decano, width / 4 - 50, firma_y, width=150, preserveAspectRatio=True, mask='auto')
    c.drawString(width / 4 - 30, firma_y - 20, cargo_decano)

    c.drawImage(firma_vicerrector, 3 * width / 4 - 50, firma_y, width=150, preserveAspectRatio=True, mask='auto')
    c.drawString(3 * width / 4 - 30, firma_y - 20, cargo_vicerrector)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer