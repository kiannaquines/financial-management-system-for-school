from django.shortcuts import render
from system.models import *
from django.db.models import Sum
from authentication.models import AuthUser


def dashboard_page(request):
    context = {}
    total_amount = 0

    total_membership = Membership.objects.filter(membership_status=True).count()
    total_pending = Membership.objects.filter(membership_status=False).count()
    total_beneficary = Beneficiary.objects.count()
    total_payments = Payment.objects.annotate(total_amount=Sum("amount")).values('total_amount')

    for total in total_payments:
        total_amount += total['total_amount']

    latest_users = AuthUser.objects.all().order_by("-last_login")[:100]
    context["total_beneficary"] = total_beneficary
    context["total_payments"] = total_amount
    context["total_pending"] = total_pending
    context["total_membership"] = total_membership
    context["latest_users"] = latest_users

    return render(request, "dashboard.html", context)