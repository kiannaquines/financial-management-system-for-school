from django.contrib import messages
from typing import Any
from django.forms import BaseModelForm
from django.shortcuts import render
from system.forms import LedgerForm, UpdateMembershipInforDependentsForm
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
from django.views.generic import View, CreateView, UpdateView, DeleteView


from django.http import HttpResponse
from django.shortcuts import render
from system.models import *
from system.utils import oneshot_view_function
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from calendar import monthrange
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


@login_required(login_url="/auth/")
def beneficiary_page(request):
    path = reverse_lazy("add_beneficiary_page")
    header_list = [
        "First Name",
        "Middle Name",
        "Last Name",
        "Suffix",
        "Relationship",
        "Date of Birth",
    ]
    field_list = [
        "id",
        "beneficiary_first_name",
        "beneficiary_middle_name",
        "beneficiary_last_name",
        "suffix",
        "relationship",
        "date_of_birth",
    ]
    context = oneshot_view_function(
        Beneficiary.objects.values(*field_list),
        "Beneficiary",
        "Beneficiaries List",
        "Add Beneficiary",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def payments_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = [
        "Firstname",
        "Lastname",
        "Employee ID",
        "Collection",
        "Payment Type",
        "Date Paid",
    ]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
        "paid_by__user_id__last_name",
        "paid_by__employee_id",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.values(*field_list),
        "Payment",
        "Payments List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def users_page(request):
    path = reverse_lazy("add_user_page")
    header_list = ["Username", "Firstname", "Lastname", "Type"]
    field_list = ["id", "username", "first_name", "last_name", "user_type"]
    context = oneshot_view_function(
        AuthUser.objects.filter(is_active=True).values(*field_list),
        "User",
        "Users List",
        "Add User",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def inactive_users_page(request):
    path = reverse_lazy("add_user_page")
    header_list = ["Username", "Firstname", "Lastname", "Email", "User Type", "Active"]
    field_list = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "user_type",
        "is_active",
    ]
    context = oneshot_view_function(
        AuthUser.objects.filter(is_active=False).values(*field_list),
        "Inactive Users",
        "Users List",
        "Add User",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def membership_page(request):
    path = reverse_lazy("add_member_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Contact Number",
        "Employee ID",
    ]
    field_list = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "contact_number",
        "employee_id",
    ]
    context = oneshot_view_function(
        Membership.objects.filter(membership_status=True).values(*field_list),
        "Membership",
        "Memberships List",
        "Enroll Member",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def pending_membership_page(request):
    path = reverse_lazy("add_member_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Contact Number",
        "Employee ID",
    ]
    field_list = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "contact_number",
        "employee_id",
    ]
    context = oneshot_view_function(
        Membership.objects.filter(membership_status=False).values(*field_list),
        "Pending Membership",
        "Pending Memberships List",
        "Add Member",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=True).values(*field_list),
        "Assistance",
        "Assistance List",
        "Add Assistance",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def pending_assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=False).values(*field_list),
        "Pending Assistance",
        "Pending Assistance List",
        "Add Assistance",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Assistance Type",
        "Amount Applied",
        "Release Status",
        "Status",
    ]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "amount_released",
        "released_status",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=True).values(*field_list),
        "Assistance",
        "Assistance List",
        "Add Assistance",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def payment_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = [
        "Firstname",
        "Lastname",
        "Employee ID",
        "Expense Type",
    ]
    field_list = [
        "id",
        "paid_by__first_name",
        "paid_by__last_name",
        "paid_by__employee_id",
        "payment_type",
    ]
    context = oneshot_view_function(
        Payment.objects.values(*field_list),
        "Payment",
        "Payment List",
        "Add Payment",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def membership_fee_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Collection", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.filter(payment_type="Membership").values(*field_list),
        "Membership Fee",
        "Membership Fee List",
        "Add Payment",
        path,
        header_list,
    )
    context["schools"] = [school[0] for school in Membership.SCHOOL_AFFILIATION]
    context["members"] = Membership.objects.all().distinct()
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def monthly_due_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.filter(
            Q(payment_type="Delegation Pay")
            | Q(payment_type="Trust Fund")
            | Q(payment_type="Visitors Fund")
        ).values(*field_list),
        "Monthly Due",
        "Monthly Due List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def dependents_page(request):
    path = reverse_lazy("add_dependent_page")
    header_list = ["Firstname","Middlename", "Lastname", "Gender","Relationship"]
    field_list = ["id", "dependent_first_name", "dependent_middle_name", "dependent_last_name", "gender", "relationship_to_member"]
    context = oneshot_view_function(
        Dependents.objects.values(*field_list),
        "Dependents",
        "Dependent List",
        "Add Dependents Expense",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def other_expense_page(request):
    path = reverse_lazy("add_expense_page_form")
    header_list = ["Expense", "Amount", "Date"]
    field_list = ["id", "expense_type", "amount", "date_added"]
    context = oneshot_view_function(
        Expenses.objects.values(*field_list),
        "Other Expense",
        "Other Expense List",
        "Add Other Expense",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url="/auth/")
def other_report_expense_page(request):
    path = reverse_lazy("generate_other_expense")
    header_list = ["Expense", "Amount", "Date"]
    field_list = ["id", "expense_type", "amount", "date_added"]
    context = oneshot_view_function(
        Expenses.objects.values(*field_list),
        "Expense",
        "Expense List",
        "Export Other Expense",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url="/auth/")
def assistance_expense_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname","Lastname", "Amount Applied", "Date Released"]
    field_list = ["id", "request_by__first_name", "request_by__last_name", "amount_released", "date_released"]
    context = oneshot_view_function(
        Assistance.objects.values(*field_list),
        "Assistance Expense",
        "Assistance Expense List",
        "Add Assistance Expense",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url="/auth/")
def assistance_report_expense_page(request):
    path = reverse_lazy("generate_assistance_expense")
    header_list = ["Firstname","Lastname", "Amount Applied", "Date Released"]
    field_list = ["id", "request_by__first_name", "request_by__last_name", "amount_released", "date_released"]
    context = oneshot_view_function(
        Assistance.objects.values(*field_list),
        "Export Assistance Expense",
        "Export Assistance Expense List",
        "Export Assistance Expense",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)


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
                extra_tags="error_tag",
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
                extra_tags="error_tag",
            )
            return redirect(reverse_lazy("membership_fee_page"))

        member_result = []
        total_paid_amount = 0

        for payment in payments:
            fullname = f"{payment.paid_by.last_name}, {payment.paid_by.first_name}"
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
            "prepared_by": f"{request.user.first_name} {request.user.last_name}",
            "report_type": f"Annual Membership Report",
        }

        template = get_template("membership_report.html")
        html = template.render(context)
        pisa.CreatePDF(html, dest=response)

        return response


class ExportLedgerView(View):
    template_name = "export_ledger.html"
    def get(self, request, *args, **kwargs):
        context = {}
        context['transactions'] = Ledger.objects.all().order_by('date_transaction')
        return render(request, self.template_name, context)
    
    def post(self, request):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A3
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import inch
        from django.http import HttpResponse
        from datetime import datetime
        import io
        

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
        
        table = Table(data, colWidths=[1*inch, 1.5*inch, 4*inch, 2*inch, 2*inch])

        
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
    template_name = "ledger.html"
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

    latest_users = AuthUser.objects.all().order_by("-last_login")[:100]
    context["total_beneficary"] = total_beneficary
    context["total_payments"] = total_amount
    context["total_pending"] = total_pending
    context["total_membership"] = total_membership
    context["latest_users"] = latest_users

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
        extra_tags="success_tag",
    )
    return HttpResponseRedirect(reverse_lazy("assistance_page"))


@login_required(login_url="/auth/")
def approve_membership(request, pk):
    membership = Membership.objects.get(id=pk)
    membership.membership_status = True
    membership.save()
    success(
        request,
        "You have successfully approved the membership request.",
        extra_tags="success_tag",
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
        extra_tags="success_tag",
    )
    return HttpResponseRedirect(reverse_lazy("users_page"))


def generate_other_expense(request):
    if request.method == "GET":
        query = Expenses.objects.all()
        result = one_shot_pdf_generation_other_expense(
            request, "other_expense_fee_report", "Other Expenses Report", query
        )
        return result
    
from django.views.generic import UpdateView

class UpdateMemberInfoDependents(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "pages/update.html"
    model = Membership
    form_class = UpdateMembershipInforDependentsForm
    success_url = reverse_lazy("employee_apply_membership")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Member"
        return context