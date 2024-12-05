from django.contrib import messages
from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from system.forms import UserMembershipForm, UserBeneficiaryForm, UserAssistanceForm, ViewUserMembershipForm
from system.models import Beneficiary, Dependents, Payment, Membership, Assistance
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from system.forms import UserMembershipForm
 
@login_required(login_url='/auth/')
def employee_apply_membership(request):
    context = {}
    form = UserMembershipForm(user=request.user)

    if request.method == "POST":
        form_data = UserMembershipForm(request.POST, user=request.user)

        if form_data.is_valid():
            membership = form_data.save(commit=False)
            
            if Membership.objects.filter(user_id=request.user).exists():
                messages.error(request,'You are already a member, you cannot request another membership.',extra_tags='danger')
                return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
            
            membership.user_id = request.user
            membership.save()
            messages.success(request,'You have successfully applied for membership, Thank you!.',extra_tags='success')

            return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
        
    context['form'] = form
    context['header_title'] = 'Enroll Member'
    return render(request,'employee/form.html',context)

@login_required(login_url='/auth/')
def employee_add_beneficiary(request):
    context = {}
    form = UserBeneficiaryForm()

    if request.method == "POST":
        form_data = UserBeneficiaryForm(request.POST, request.FILES)

        if form_data.is_valid():
            beneficiary = form_data.save(commit=False)

            query_my_membership = Membership.objects.filter(
                user_id=request.user,
            ).first()

            if not query_my_membership:
                messages.error(request,'You are not a member, you cannot add a beneficiary.',extra_tags='danger')
                return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))

            beneficiary.user_id = query_my_membership
            beneficiary.save()
            
            messages.success(request,'You have successfully added you beneficiary',extra_tags='success')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))
        else:
            messages.error(request,'There is something wrong in adding your beneficiary, please try again.',extra_tags='success')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))

    context['form'] = form
    context['header_title'] = 'Add Beneficiary'
    return render(request,'employee/form.html',context)

@login_required(login_url='/auth/')
def employee_apply_assistance(request):
    context = {}
    form = UserAssistanceForm()

    if request.method == "POST":
        form_data = UserAssistanceForm(request.POST, request.FILES)

        if form_data.is_valid():
            assistance_data = form_data.save(commit=False)
            query_my_membership = Membership.objects.filter(
                user_id=request.user,
            ).first()

            if not query_my_membership:
                messages.error(request,'You are not a member, you cannot request assistance.',extra_tags='danger')
                return HttpResponseRedirect(reverse_lazy('employee_assistance_request'))

            assistance_data.request_by = query_my_membership
            assistance_data.save()
            messages.success(request,'You have successfully applied for assistance, please wait until the president of the association approve your request. Thank you!.',extra_tags='warning')
            return HttpResponseRedirect(reverse_lazy('employee_assistance_request'))
        else:
            messages.error(request,'There is something wrong in applying for assistance, please try again.',extra_tags='danger')
            return HttpResponseRedirect(reverse_lazy('employee_view_payments'))
        
    context['form'] = form
    context['header_title'] = "Apply Assistance"
    return render(request,'employee/form.html',context)

@login_required(login_url='/auth/')
def employee_view_beneficiary(request):
    context = {}
    context['items'] = Beneficiary.objects.filter(user_id__user_id=request.user)
    return render(request,'employee/my_beneficiary.html',context)


@login_required(login_url='/auth/')
def employee_view_dependents(request):
    context = {}
    context['items'] = Dependents.objects.filter(related_to_member__user_id=request.user)
    return render(request,'employee/my_dependents.html',context)

@login_required(login_url='/auth/')
def employee_view_payments(request):
    context = {}
    context['items'] = Payment.objects.filter(paid_by__user_id=request.user)
    return render(request,'employee/my_payments.html',context)

@login_required(login_url='/auth/')
def employee_assistance_request(request):
    context = {}
    context['my_assistance_request'] = Assistance.objects.filter(request_by__user_id=request.user)
    return render(request,'employee/my_assistance.html',context)



def my_membership(request, pk):
    membership = Membership.objects.filter(user_id=pk).first()

    if not membership:
        messages.error(request, "No associated membership for your account, please try again.", extra_tags="danger")
        return redirect('employee_apply_membership')

    user_membership_form = ViewUserMembershipForm(instance=membership, user=request.user.membership)
    context = {
        'user_membership_form': user_membership_form,
        'membership_id': membership.id,
    }

    return render(request, 'employee/membership_details.html', context)

    
    