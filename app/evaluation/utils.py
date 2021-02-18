from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration


def render_to_pdf(template_src, context_dict={}):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=evaluation.pdf"
    html = render_to_string(template_src, context_dict)
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response
