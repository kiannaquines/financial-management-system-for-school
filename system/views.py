from django.shortcuts import render
from system.models import *
from django.db.models import Sum

def dashboard_page(request):
    context = {}
    total_membership = Membership.objects.filter(membership_status=True).count()
    total_pending = Membership.objects.filter(membership_status=False).count()
    total_beneficary = Beneficiary.objects.count()
    total_payments = Payment.objects.annotate(total_amount=Sum('amount')).count()
    context['total_beneficary'] = total_beneficary
    context['total_payments'] = total_payments
    context['total_pending'] = total_pending
    context['total_membership'] = total_membership

    return render(request, 'dashboard.html', context)