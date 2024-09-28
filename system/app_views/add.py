from django.shortcuts import render
from system.models import *
from system.forms import *
from authentication.forms import RegistrationForm
from system.utils import oneshot_add_function
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error

def add_beneficiary_page(request):
    path = reverse_lazy('beneficiary_page')

    if request.method == "POST":
        form_data = BeneficiaryForm(request.POST, request.FILES)
        
        if form_data.is_valid():
            beneficiary = form_data.save(commit=False)
            beneficiary.user_id = request.user
            beneficiary.save()
            success(request,'You have successfully added new beneficiary.', extra_tags="success_tag")
            return HttpResponseRedirect(path)
        else:
            error(request,'There is an error in adding your beneficiary, please try again.', extra_tags='error_tag')
            return HttpResponseRedirect(path)
        
    form = BeneficiaryForm()
    context = oneshot_add_function(form, 'Add Beneficiary', 'Beneficiary Management', 'Add Beneficiary')
    return render(request, 'pages/add.html',context)

def add_member_page(request):
    path = reverse_lazy('membership_page')
    if request.method == "POST":
        form_data = MembershipForm(request.POST)

        if form_data.is_valid():
            
            selected_beneficiaries = form_data['beneficiary'].value()

            for id in selected_beneficiaries:
                beneficiary_status = Beneficiary.objects.get(beneficiary_id=id)
                beneficiary_status.used = True
                beneficiary_status.save()

            membership_data = form_data.save(commit=False)
            membership_data.user_id = request.user
            membership_data.save()

            success(request,'You have successfully added new membership.', extra_tags="success_tag")
            return HttpResponseRedirect(path)
        
        else:
            
            error(request,'There is an error in adding your membership, please try again.', extra_tags='error_tag')
            return HttpResponseRedirect(path)
        
    form = MembershipForm()
    context = oneshot_add_function(form, 'Add Membership', 'Membership Management', 'Add Membership')
    return render(request, 'pages/add.html',context)

def add_payment_page(request):

    if request.method == "POST":
        pass

    form = PaymentForm()
    context = oneshot_add_function(form, 'Add Payment', 'Payment Management', 'Add Payment')
    return render(request, 'pages/add.html', context)

def add_user_page(request):

    if request.method == "POST":
        pass

    form = RegistrationForm()
    context = oneshot_add_function(form, 'Add User', 'User Management', 'Add User')
    return render(request, 'pages/add.html',context)
