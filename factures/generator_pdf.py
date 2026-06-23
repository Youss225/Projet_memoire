from io import BytesIO
import base64
import qrcode

from django.template.loader import render_to_string
from weasyprint import HTML


def generate_facture_pdf(request, facture):
    """
    Génère un PDF professionnel PETRO DISTRIBUTIONS
    avec QR Code intégré.
    """

    # -----------------------------
    # URL de consultation facture
    # -----------------------------
    facture_url = request.build_absolute_uri(
        f"/factures/{facture.id}/preview/"
    )

    # -----------------------------
    # Génération QR Code
    # -----------------------------
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )

    qr.add_data(facture_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    qr_code = f"data:image/png;base64,{qr_base64}"

    # -----------------------------
    # Logo
    # -----------------------------
    logo_url = request.build_absolute_uri("/media/Logo.jpg")

    # -----------------------------
    # HTML template
    # -----------------------------
    html_string = render_to_string(
        "facture.html",
        {
            "facture": facture,
            "client": facture.client,
            "lignes": facture.lignes.all(),
            "logo_url": logo_url,
            "qr_code": qr_code,
            "entreprise": "PETRO DISTRIBUTIONS",
            "telephone": "+225 59 59 57 89",
            "email": "contact@petrodistributions.com",
            "adresse": "Abidjan - Côte d’Ivoire",
        }
    )

    # -----------------------------
    # Génération PDF
    # -----------------------------
    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    return pdf_file