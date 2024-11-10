from django.shortcuts import render
from system.models import *
from django.db.models import Sum
from authentication.models import AuthUser
from system.utils import one_shot_pdf_generation, one_shot_pdf_generation_expense
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages import success
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import TruncMonth


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
        request, "expense_fee_report", "Expenses Report", query
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
