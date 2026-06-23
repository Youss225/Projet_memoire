from django.template.loader import render_to_string
from weasyprint import HTML
import imgkit

def render_facture_html(facture):
    html = render_to_string('facture.html', {
        'facture': facture,
        'client': facture.client,
        'lignes': facture.lignes.all(),
        'logo_url': 'http://127.0.0.1:8000/media/logo.png'
    })
    return html


def generate_pdf(facture):
    html = render_facture_html(facture)
    pdf = HTML(string=html).write_pdf()
    return pdf


def generate_image(facture):
    html = render_facture_html(facture)
    imgkit.from_string(html, 'facture.png')
    return 'facture.png'