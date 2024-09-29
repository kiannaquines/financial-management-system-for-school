from django.http import HttpResponseRedirect
from django.shortcuts import render
from system.forms import UserMembershipForm, UserBeneficiaryForm, UserAssistanceForm
from system.models import Beneficiary, Payment, Membership, Assistance
from django.contrib.messages import error, success
from django.urls import reverse_lazy


def employee_apply_membership(request):
    context = {}
    form = UserMembershipForm()

    if request.method == "POST":
        form_data = UserMembershipForm(request.POST)

        if form_data.is_valid():
            membership = form_data.save(commit=False)
            
            if Membership.objects.filter(user_id=request.user).exists():
                error(request,'You are already a member, you cannot request another membership.',extra_tags='error_tag')
                return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
            
            membership.user_id = request.user
            membership.save()
            success(request,'You have successfully applied for membership, Thank you!.',extra_tags='error_tag')

            return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
        
    context['form'] = form
    context['header_title'] = "Apply Membership"
    return render(request,'employee/add.html',context)

def employee_add_beneficiary(request):
    context = {}
    form = UserBeneficiaryForm()

    if request.method == "POST":
        form_data = UserBeneficiaryForm(request.POST, request.FILES)

        if form_data.is_valid():
            beneficiary = form_data.save(commit=False)
            beneficiary.user_id = request.user
            beneficiary.save()
            
            success(request,'You have successfully added you beneficiary',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))
        else:
            error(request,'There is something wrong in adding your beneficiary, please try again.',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))

    context['form'] = form
    context['header_title'] = "Add Beneficiary"
    return render(request,'employee/add.html',context)

def employee_apply_assistance(request):
    context = {}
    form = UserAssistanceForm()

    if request.method == "POST":
        form_data = UserAssistanceForm(request.POST, request.FILES)

        if form_data.is_valid():
            assistance_data = form_data.save(commit=False)
            assistance_data.request_by = request.user
            assistance_data.save()
            success(request,'You have successfully applied for assistance, Thank you!.',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_payments'))
        else:
            error(request,'There is something wrong in applying for assistance, please try again.',extra_tags='error_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_payments'))
        
    context['form'] = form
    context['header_title'] = "Apply Assistance"
    return render(request,'employee/add.html',context)

def employee_view_beneficiary(request):
    context = {}
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
    context['view_data'] = Beneficiary.objects.filter(user_id=request.user).values(*field_list)
    context['header_title'] = "My Beneficiaries"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)

def employee_view_payments(request):
    context = {}
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__username",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context['view_data'] = Payment.objects.filter(paid_by=request.user).values(*field_list)
    context['header_title'] = "My Payments"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)


def employee_assistance_request(request):
    context = {}
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context['view_data'] = Assistance.objects.filter(request_by=request.user).values(*field_list)
    context['header_title'] = "My Assistance Request"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)