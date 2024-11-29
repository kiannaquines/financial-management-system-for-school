from django.contrib import messages
from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from system.forms import UserMembershipForm, UserBeneficiaryForm, UserAssistanceForm, ViewUserMembershipForm
from system.models import Beneficiary, Payment, Membership, Assistance
from django.contrib.messages import error, success
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView, View
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
                error(request,'You are already a member, you cannot request another membership.',extra_tags='error_tag')
                return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
            
            membership.user_id = request.user
            membership.save()
            success(request,'You have successfully applied for membership, Thank you!.',extra_tags='success_tag')

            return HttpResponseRedirect(reverse_lazy('employee_apply_membership'))
        
    context['form'] = form
    context['header_title'] = "Apply Membership"
    return render(request,'employee/add.html',context)

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
                error(request,'You are not a member, you cannot add a beneficiary.',extra_tags='error_tag')
                return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))

            beneficiary.user_id = query_my_membership
            beneficiary.save()
            
            success(request,'You have successfully added you beneficiary',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))
        else:
            error(request,'There is something wrong in adding your beneficiary, please try again.',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_beneficiary'))

    context['form'] = form
    context['header_title'] = "Add Beneficiary"
    return render(request,'employee/add.html',context)

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
                error(request,'You are not a member, you cannot request assistance.',extra_tags='error_tag')
                return HttpResponseRedirect(reverse_lazy('employee_assistance_request'))

            assistance_data.request_by = query_my_membership
            assistance_data.save()
            success(request,'You have successfully applied for assistance, Thank you!.',extra_tags='success_tag')
            return HttpResponseRedirect(reverse_lazy('employee_assistance_request'))
        else:
            error(request,'There is something wrong in applying for assistance, please try again.',extra_tags='error_tag')
            return HttpResponseRedirect(reverse_lazy('employee_view_payments'))
        
    context['form'] = form
    context['header_title'] = "Apply Assistance"
    return render(request,'employee/add.html',context)

@login_required(login_url='/auth/')
def employee_view_beneficiary(request):
    context = {}
    header_list = [
        "First Name",
        "Last Name",
        "Suffix",
        "Relationship",
        "Date of Birth",
    ]
    field_list = [
        "id",
        "beneficiary_first_name",
        "beneficiary_last_name",
        "suffix",
        "relationship",
        "date_of_birth",
    ]
    context['view_data'] = Beneficiary.objects.filter(user_id__user_id=request.user).values(*field_list)
    context['header_title'] = "My Beneficiaries"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)

@login_required(login_url='/auth/')
def employee_view_payments(request):
    context = {}
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context['view_data'] = Payment.objects.filter(paid_by__user_id=request.user).values(*field_list)
    context['header_title'] = "My Payments"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)

@login_required(login_url='/auth/')
def employee_assistance_request(request):
    context = {}
    header_list = ["Firstname", "Middlename", "Lastname","Amount Released", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "amount_released",
        "type_of_assistance",
        "assistance_status",
    ]
    context['view_data'] = Assistance.objects.filter(request_by__user_id=request.user).values(*field_list)
    context['header_title'] = "My Assistance Request"
    context['header_list'] = header_list
    return render(request,'employee/view.html',context)



def my_membership(request, pk):
    membership = Membership.objects.filter(user_id=pk).first()

    if not membership:
        messages.error(request, "No associated membership for your account, please try again.")
        return redirect('employee_apply_membership')

    user_membership_form = ViewUserMembershipForm(instance=membership)

    context = {
        'user_membership_form': user_membership_form
    }
    
    return render(request, 'employee/membership_details.html', context)

class BeneficiaryUpdateView(UpdateView):
    model = Beneficiary
    form_class = UserBeneficiaryForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employee_view_beneficiary')
    template_name = 'employee/update.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Update Beneficiary Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Beneficiary details updated successfully.",
            extra_tags="success_tag",
        )
        return form
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                error(
                    self.request,
                    f"{error}",
                    extra_tags="error_tag",
                )
        return super().form_invalid(form)
    

class BeneficiaryDeleteView(DeleteView):
    model = Beneficiary
    success_url = reverse_lazy('employee_view_beneficiary')
    template_name = 'employee/delete.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Remove Beneficiary Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Beneficiary details removed successfully.",
            extra_tags="success_tag",
        )
        return form


class AssistanceUpdateView(UpdateView):
    model = Assistance
    form_class = UserAssistanceForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employee_assistance_request')
    template_name = 'employee/update.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Update Assistance Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success_tag",
        )
        return form
    

class AssistanceDeleteView(DeleteView):
    model = Assistance
    success_url = reverse_lazy('employee_assistance_request')
    template_name = 'employee/delete.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Remove Assistance Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Assistance details removed successfully.",
            extra_tags="success_tag",
        )
        return form