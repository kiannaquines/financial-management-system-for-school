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

class DeleteTransactionToLedger(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'pages/delete.html'
    model = Ledger
    success_url = reverse_lazy('ledger_list')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = 'Delete Transaction'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            'You have successfully remove transaction to the ledger.',
            extra_tags='success_tag'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)



class UpdateTransactionToLedger(UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'pages/add.html'
    model = Ledger
    form_class = LedgerForm
    success_url = reverse_lazy('ledger_list')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = 'Update Transaction'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.recorded_by = self.request.user
        messages.success(
            self.request,
            'You have successfully updated transaction to the ledger.',
            extra_tags='success_tag'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class AddTransactionToLedger(CreateView):
    template_name = 'pages/add.html'
    model = Ledger
    form_class = LedgerForm
    success_url = reverse_lazy('ledger_list')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = 'Add Transaction'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.recorded_by = self.request.user
        messages.success(
            self.request,
            'You have successfully added a new transaction to the ledger.',
            extra_tags='success_tag'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

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