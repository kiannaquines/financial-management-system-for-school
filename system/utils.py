import os
from django.template.loader import get_template
from authentication.models import AuthUser
from xhtml2pdf import pisa
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from authentication.models import AuthUser


def one_shot_pdf_generation(request, filename, title, query):

    context = {}

    current_date = datetime.now()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{filename}-{current_date}.pdf"'
    )

    total_amount = 0
    for item in query:
        total_amount += item.amount

    context["date_generated"] = current_date
    context["generated_by"] = AuthUser.get_full_name(request.user)
    context["logo_path"] = ''
    context["query_info"] = query
    context["title"] = title
    context['total_amount_paid'] = f'{total_amount:,}'
    template = get_template("pdf_template/template.html")

    rendered_html = template.render(context)
    createPDF = pisa.CreatePDF(rendered_html, dest=response)

    if createPDF.err:
        return HttpResponse("Error generating PDF: %s" % createPDF.err)

    return response


def one_shot_pdf_generation_expense(request, filename, title, query):

    context = {}

    total_amount = 0
    for item in query:
        total_amount += item.amount_released

    current_date = datetime.now()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{filename}-{current_date}.pdf"'
    )
    context["date_generated"] = current_date
    context["generated_by"] = AuthUser.get_full_name(request.user)
    context["logo_path"] = ''
    context["expenses"] = query
    context["title"] = title
    context['total_amount'] = f'{total_amount:,}'
    template = get_template("pdf_template/expense_template.html")

    rendered_html = template.render(context)
    createPDF = pisa.CreatePDF(rendered_html, dest=response)

    if createPDF.err:
        return HttpResponse("Error generating PDF: %s" % createPDF.err)

    return response


def one_shot_pdf_generation_other_expense(request, filename, title, query):

    context = {}
    
    total_amount = 0
    for item in query:
        total_amount += item.amount

    current_date = datetime.now()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{filename}-{current_date}.pdf"'
    )
    context["date_generated"] = current_date
    context["generated_by"] = AuthUser.get_full_name(request.user)
    context["logo_path"] = ''
    context["expenses"] = query
    context["title"] = title
    context['total_amount'] = f'{total_amount:,}'
    template = get_template("pdf_template/other_expense_template.html")

    rendered_html = template.render(context)
    createPDF = pisa.CreatePDF(rendered_html, dest=response)

    if createPDF.err:
        return HttpResponse("Error generating PDF: %s" % createPDF.err)

    return response