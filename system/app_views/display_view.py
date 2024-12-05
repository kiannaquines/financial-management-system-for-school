from django.contrib import messages
from typing import Any
from django.shortcuts import render
from system.models import *
from django.db.models import Sum
from authentication.models import AuthUser
from system.utils import one_shot_pdf_generation, one_shot_pdf_generation_expense, one_shot_pdf_generation_other_expense
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages import success
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.views.generic import View

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from datetime import datetime
import io

from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from calendar import monthrange
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
import json


# DONE
@login_required(login_url="/auth/")
def membership_page(request):
    context = {}
    enrolled_membership = Membership.objects.filter(membership_status=True)
    context['enrolled_members'] = enrolled_membership
    return render(request, "view_template/enrolled_members.html", context)

# DONE
@login_required(login_url="/auth/")
def pending_membership_page(request):
    context = {}
    pending_membership = Membership.objects.filter(membership_status=False)
    context['pending_members'] = pending_membership   
    return render(request, "view_template/pending_members.html", context)


@login_required(login_url="/auth/")
def users_page(request):
    context = {}
    users = AuthUser.objects.filter(is_active=True)
    context['users'] = users
    return render(request, "view_template/users.html", context)

@login_required(login_url="/auth/")
def beneficiary_page(request):
    context = {}
    path = reverse_lazy("add_beneficiary_page")
    
    context['beneficiary'] = Beneficiary.objects.all()
    return render(request, "view_template/beneficiaries.html", context)


@login_required(login_url="/auth/")
def payments_page(request):
    context = {}
    context['payments'] =  Payment.objects.all()
    return render(request, "view_template/payment.html", context)


@login_required(login_url="/auth/")
def inactive_users_page(request):
    context = {}
    context['users'] = AuthUser.objects.filter(is_active=False)
    return render(request, "view_template/inactive_users.html", context)


@login_required(login_url="/auth/")
def pending_assistance_page(request):
    context = {}
    pending_assistance = Assistance.objects.filter(assistance_status=False).all()
    context['pending_assistance'] = pending_assistance
    return render(request, "view_template/pending_assistance.html",context)


@login_required(login_url="/auth/")
def assistance_page(request):
    context = {}
    assistance = Assistance.objects.filter(assistance_status=True)
    context['assistance'] = assistance
    return render(request, "view_template/assistance.html", context)


@login_required(login_url="/auth/")
def payment_page(request):
    context = {}
    payments = Payment.objects.all()
    context["payments"] = payments
    return render(request, "view_template/payment.html", context)


@login_required(login_url="/auth/")
def membership_fee_page(request):
    context = {}
    context["membership_fee"] = Payment.objects.filter(payment_type="Membership").all()
    context["schools"] = [school[0] for school in Membership.SCHOOL_AFFILIATION]
    context["members"] = Membership.objects.all().distinct()
    return render(request, "view_template/membership_fee.html", context)


@login_required(login_url="/auth/")
def monthly_due_page(request):
    context = {}
    context['monthly_dues'] =  Payment.objects.filter(Q(payment_type="Delegation Pay") | Q(payment_type="Trust Fund") | Q(payment_type="Visitors Fund"))
    return render(request, "view_template/monthly_due.html", context)


@login_required(login_url="/auth/")
def dependents_page(request):
    context = {}
    context["dependents"] = Dependents.objects.all()
    return render(request, "view_template/dependents.html", context)


@login_required(login_url="/auth/")
def other_expense_page(request):
    context = {}
    expenses = Expenses.objects.all()
    context['expenses'] = expenses
    return render(request, "view_template/other_expenses.html", context)


@login_required(login_url="/auth/")
def school_page(request):
    context = {}
    context['items'] = SchoolYear.objects.all()
    return render(request, "view_template/school_year.html", context)

@login_required(login_url="/auth/")
def other_report_expense_page(request):
    context = {}
    other_expenses = Expenses.objects.all()
    context['items'] = other_expenses
    return render(request, "view_template/expenses.html", context)

@login_required(login_url="/auth/")
def assistance_expense_page(request):
    context = {}
    assistance = Assistance.objects.filter(assistance_status=True).all()
    context["assistance"] = assistance
    return render(request, "view_template/assistance_expenses.html", context)

@login_required(login_url="/auth/")
def assistance_report_expense_page(request):
    context = {}
    assistance = Assistance.objects.all()
    context["assistance"] = assistance
    return render(request, "view_template/assistance_release_expense.html", context)


def is_exactly_11_months(start_date, end_date):
    months_difference = (end_date.year - start_date.year) * 11 + (
        end_date.month - start_date.month
    )
    print(months_difference)
    return months_difference == 11


@login_required(login_url="/auth/")
def generate_annual_membership_report(request):
    if request.method == "POST":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="annual_membership_payment.pdf"'
        )

        school_year_from = request.POST.get("range_from")
        school_year_to = request.POST.get("range_to")
        school = request.POST.get("school")
        member_id = request.POST.get("member")

        start_date = timezone.make_aware(
            datetime.strptime(school_year_from, "%Y-%m-%d")
        )
        end_date = timezone.make_aware(datetime.strptime(school_year_to, "%Y-%m-%d"))

        if not is_exactly_11_months(start_date, end_date):
            messages.warning(
                request,
                "The selected date range is incorrect, please try again.",
                extra_tags="danger",
            )
            return redirect(reverse_lazy("membership_fee_page"))

        month_headers = []
        current_date = start_date
        while current_date <= end_date:
            month_headers.append(current_date.strftime("%m"))
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(
                day=1
            )

        payments = Payment.objects.filter(
            date_paid__range=(start_date, end_date),
            payment_type="Membership",
        )

        if school and school != "All":
            payments = payments.filter(paid_by__school_affiliation=school)

        if member_id:
            payments = payments.filter(paid_by=member_id)

        if not payments.exists():
            messages.warning(
                request,
                "No membership payment found using the provided date range and school, please try again later.",
                extra_tags="danger",
            )
            return redirect(reverse_lazy("membership_fee_page"))

        member_result = []
        total_paid_amount = 0

        for payment in payments:
            fullname = f"{payment.paid_by}"
            monthly_payments = {month: 0 for month in month_headers}
            current_date = start_date
            member_total_paid = 0

            while current_date <= end_date:
                month_start = current_date.replace(day=1)
                last_day = monthrange(current_date.year, current_date.month)[1]
                month_end = current_date.replace(day=last_day)

                month_payments = Payment.objects.filter(
                    date_paid__range=(month_start, month_end),
                    payment_type="Membership",
                    paid_by=payment.paid_by,
                )

                total_paid = month_payments.aggregate(total=Sum("amount"))["total"] or 0
                monthly_payments[current_date.strftime("%m")] = f"{int(total_paid):,}"
                member_total_paid += int(total_paid)
                current_date += timedelta(days=last_day)

            member_result.append(
                {
                    "fullname": fullname,
                    "monthly_payments": monthly_payments,
                    "total_paid": f"{int(member_total_paid):,}",
                }
            )

            total_paid_amount += member_total_paid

        context = {
            "school": school,
            "month_headers": month_headers,
            "member_result": member_result,
            "school_year": f"SCHOOL YEAR {start_date.year} - {end_date.year}",
            "total_amount": f"{total_paid_amount:,}",
            "report_date": timezone.now().strftime("%B %d, %Y"),
            "prepared_by": f"{request.user.get_full_name()}",
            "report_type": f"Annual Membership Report",
        }

        template = get_template("pdf_template/membership_report.html")
        html = template.render(context)
        pisa.CreatePDF(html, dest=response)

        return response


class ExportLedgerView(View):
    template_name = "view_template/export_ledger.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['transactions'] = Ledger.objects.all().order_by('date_transaction')
        return render(request, self.template_name, context)
    
    def post(self, request):
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A3,
            rightMargin=40,
            leftMargin=40,
            topMargin=10,
            bottomMargin=72
        )
        doc.title = 'DSAPSTEA Financial Management Ledger'
        
        elements = []
        custom_blue = colors.HexColor('#014171')
        custom_grid_color = colors.HexColor('#f5f5f5')
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=custom_blue,
        )
        
        title = Paragraph("DSAPSTEA FINANCIAL LEDGER", title_style)
        elements.append(title)
                
        transactions = Ledger.objects.all().order_by('transaction_date')
        
        data = [['No', 'Date', 'Description', 'Collection', 'Expense']]
        
        total_income = 0
        total_expense = 0
        
        for idx, trans in enumerate(transactions, 1):
            amount = abs(trans.amount)
            if trans.transaction_type == "Credit":
                income = f"{amount:,.2f}"
                expense = ""
                total_income += amount
            else:
                income = ""
                expense = f"{amount:,.2f}"
                total_expense += amount
                
            data.append([
                str(idx),
                trans.transaction_date.strftime('%d/%m/%Y'),
                trans.description,
                income,
                expense
            ])
        
        data.append(['TOTALS:', '', '', f'P {total_income:,.2f}', f'P {total_expense:,.2f}'])
        
        balance = total_income - total_expense
        data.append(['BALANCE:', '', '', f'P {balance:,.2f}', ''])
        
        table = Table(data, colWidths=[1*inch, 1.5*inch, 6*inch, 1.1*inch, 1.1*inch])

        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), custom_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -2), (-1, -1), colors.transparent),
            ('TEXTCOLOR', (0, -2), (-1, -1), custom_blue),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -2), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -2), 1, custom_grid_color),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (2, -1), 'LEFT'),
        ])
        table.setStyle(style)
        
        elements.append(table)
        
        doc.build(elements)
        
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="accounting_ledger.pdf"'
        response.write(pdf)
        
        return response


class LedgerView(View):
    template_name = "view_template/ledger.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['transactions'] = Ledger.objects.all().order_by('date_transaction')
        return render(request, self.template_name, context)


def membership_statistics(request):
    school_affiliation_counts = Membership.objects.values('school_affiliation').annotate(count=Count('school_affiliation')).order_by('school_affiliation')
    school_affiliation_data = {affiliation['school_affiliation']: affiliation['count'] for affiliation in school_affiliation_counts}
    
    return JsonResponse(school_affiliation_data)


def assistance_statistics(request):
    hospitalization_count = Assistance.objects.filter(type_of_assistance="Hospitalization").count()
    death_count = Assistance.objects.filter(type_of_assistance="Death").count()

    assistance_data = {
        'hospitalization_count': hospitalization_count,
        'death_count': death_count,
    }

    return JsonResponse(assistance_data)

@login_required(login_url="/auth/")
def get_monthly_payment_data(request):
    current_year = datetime.now().year

    payments_data = (
        Payment.objects.filter(date_paid__year=current_year)
        .annotate(month=TruncMonth("date_paid"))
        .values("month", "payment_type")
        .annotate(total_amount=Sum("amount"))
        .order_by("month")
    )

    payment_by_month = {
        "Membership": [0] * 12,
        "Delegation Pay": [0] * 12,
        "Trust Fund": [0] * 12,
        "Visitors Fund": [0] * 12,
    }

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    for payment in payments_data:
        month_index = payment["month"].month - 1
        payment_by_month[payment["payment_type"]][month_index] = payment["total_amount"]

    return JsonResponse({"payment_data": payment_by_month, "months": months})


@login_required(login_url="/auth/")
def dashboard_page(request):
    context = {}
    total_amount = 0

    total_membership = Membership.objects.filter(membership_status=True).count()
    total_pending = Membership.objects.filter(membership_status=False).count()
    total_beneficary = Beneficiary.objects.count()
    total_payments = Payment.objects.annotate(total_amount=Sum("amount")).values(
        "total_amount"
    )

    for total in total_payments:
        total_amount += total["total_amount"]

    latest_users = AuthUser.objects.all().filter(user_type="Employee").order_by("-last_login")[:100]
    context["total_beneficary"] = total_beneficary
    context["total_payments"] = total_amount
    context["total_pending"] = total_pending
    context["total_membership"] = total_membership
    context["latest_users"] = latest_users
    context["school_years"] = SchoolYear.objects.all()
    return render(request, "dashboard.html", context)


@login_required(login_url="/auth/")
def generate_annual_fee(request):
    query = Payment.objects.filter(payment_type="Membership").order_by("date_paid")
    result = one_shot_pdf_generation(
        request, "annual_membership_fee_report", "Annual Membership Fee Report", query
    )
    return result


@login_required(login_url="/auth/")
def generate_expense_fee(request):
    query = Assistance.objects.filter(
        Q(assistance_status=True) & Q(amount_released__gt=0)
    ).all()
    result = one_shot_pdf_generation_expense(
        request, "expense_fee_report", "Assistance Expenses Report", query
    )
    return result


@login_required(login_url="/auth/")
def generate_dues_fee(request):

    query = Payment.objects.filter(
        Q(payment_type="Delegation Pay")
        | Q(payment_type="Trust Fund")
        | Q(payment_type="Visitors Fund")
    ).order_by("date_paid")
    result = one_shot_pdf_generation(
        request, "monthly_dues_report", "Monthly Dues Report", query
    )
    return result


@login_required(login_url="/auth/")
def approve_assistance(request, pk):
    assistance = Assistance.objects.get(id=pk)
    assistance.assistance_status = True
    assistance.save()
    success(
        request,
        "You have successfully approved the assistance request.",
        extra_tags="success",
    )
    return HttpResponseRedirect(reverse_lazy("pending_assistance_page"))


@login_required(login_url="/auth/")
def approve_membership(request, pk):
    membership = Membership.objects.get(id=pk)
    membership.membership_status = True
    membership.save()
    success(
        request,
        "You have successfully approved the membership request.",
        extra_tags="success",
    )
    return HttpResponseRedirect(reverse_lazy("membership_page"))


@login_required(login_url="/auth/")
def activate_user(request, pk):
    user = AuthUser.objects.get(id=pk)
    user.is_active = True
    user.save()
    success(
        request,
        "You have successfully activated the user acount.",
        extra_tags="success",
    )
    return HttpResponseRedirect(reverse_lazy("users_page"))


def generate_other_expense(request):
    if request.method == "GET":
        query = Expenses.objects.all()
        result = one_shot_pdf_generation_other_expense(
            request, "other_expense_fee_report", "Other Expenses Report", query
        )
        return result
    


@login_required(login_url="/auth/")
def fetch_dashboard_data_by_school_year(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            school_year_id = data.get("school_year_id")

            if not school_year_id:
                return JsonResponse({"error": "school_year_id is required"}, status=400)

            try:
                school_year = SchoolYear.objects.get(id=school_year_id)
            except SchoolYear.DoesNotExist:
                return JsonResponse({"error": "Invalid school_year_id"}, status=404)

            payments_data = (
                Payment.objects.filter(school_year=school_year)
                .annotate(month=TruncMonth("date_paid"))
                .values("month", "payment_type")
                .annotate(total_amount=Sum("amount"))
                .order_by("month")
            )

            payment_by_month = {
                "Membership": [0] * 12,
                "Delegation Pay": [0] * 12,
                "Trust Fund": [0] * 12,
                "Visitors Fund": [0] * 12,
            }

            for payment in payments_data:
                month_index = payment['month'].month - 1
                payment_type = payment['payment_type']
                if payment_type in payment_by_month:
                    payment_by_month[payment_type][month_index] = payment['total_amount']

            months = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]


            hospitalization_count = Assistance.objects.filter(type_of_assistance="Hospitalization", date_released__range=(
                school_year.start_year, school_year.end_year
            )).count()
            death_count = Assistance.objects.filter(type_of_assistance="Death", date_released__range=(
                school_year.start_year, school_year.end_year
            )).count()

            school_affiliation_counts = Membership.objects.filter(
                school_year=school_year,
            ).values('school_affiliation').annotate(count=Count('school_affiliation')).order_by('school_affiliation')
            school_affiliation_data = {affiliation['school_affiliation']: affiliation['count'] for affiliation in school_affiliation_counts}

            total_membership = Membership.objects.filter(membership_status=True, school_year=school_year).count()
            total_pending = Membership.objects.filter(membership_status=False, school_year=school_year).count()
            total_beneficary = Beneficiary.objects.count()
            total_payments = Payment.objects.filter(
                school_year=school_year
            ).annotate(total_amount=Sum("amount")).values(
                "total_amount"
            )

            total_amount = 0
            for total in total_payments:
                total_amount += total["total_amount"]
            
            return JsonResponse({
                "total_membership": total_membership,
                "total_pending": total_pending,
                "total_beneficary": total_beneficary,
                "total_payments": total_amount,
                "payment_data": payment_by_month,
                "months": months,
                'hospitalization_count': hospitalization_count,
                'death_count': death_count,
                "school_affiliation_data": school_affiliation_data
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)