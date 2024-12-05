from django.contrib import messages
from typing import Any
from django.forms import BaseModelForm
from system.models import *
from system.forms import *
from authentication.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages import success, error
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from system.mixins import CustomLoginRequiredMixin


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
            extra_tags='success'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class BeneficiaryUpdateView(UpdateView):
    model = Beneficiary
    form_class = UserBeneficiaryForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employee_view_beneficiary')
    template_name = 'employee/form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Update Beneficiary Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Beneficiary details updated successfully.",
            extra_tags="success",
        )
        return form
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                error(
                    self.request,
                    f"{error}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class AssistanceUpdateView(UpdateView):
    model = Assistance
    form_class = UserAssistanceForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employee_assistance_request')
    template_name = 'employee/form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header_title'] = "Update Assistance Details"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success",
        )
        return form


class UpdateMemberInfoDependents(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "pages/form.html"
    model = Membership
    form_class = UpdateMembershipInforDependentsForm
    success_url = reverse_lazy("employee_apply_membership")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return Membership.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Member Information"
        return context


class UpdateDependentsView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = 'pages/form.html'
    model = Dependents
    form_class = DependentForm
    success_url = reverse_lazy("dependents_page")


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        success(
            self.request,
            "Dependent details updated successfully.",
            extra_tags="success",
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Dependent Details"
        return context
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class UpdatePasswordDetails(CustomLoginRequiredMixin, PasswordChangeView):
    pk_url_kwarg = "pk"
    model = AuthUser
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Change Password Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        success(self.request, "Password details updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return super().form_invalid(form)


class UpdateAssistanceDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Assistance
    form_class = AssistanceForm
    success_url = reverse_lazy("assistance_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Assistance Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response


class UpdateUserDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = AuthUser
    form_class = AdminRegistrationForm
    success_url = reverse_lazy("users_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update User Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request, "User details updated successfully.", extra_tags="success"
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response


class UpdatePaymentDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy("payments_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Payment Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Payment details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response


class UpdateBeneficiaryDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Beneficiary
    form_class = BeneficiaryForm
    success_url = reverse_lazy("beneficiary_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Beneficiary Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Beneficiary details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response


class UpdateMembershipDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy("membership_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Membership Details"
        return context
    


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Membership details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response


from django.db.models import Sum

class UpdateAssistanceReleaseStatusDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Assistance
    form_class = AssistanceReleaseStatusForm
    success_url = reverse_lazy("assistance_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Assistance Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:

        sum_of_collections = Payment.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0

        if form.cleaned_data['amount_released'] > sum_of_collections:
            error(
                self.request,
                "Insufficient funds available for this transaction",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("assistance_page"))
        
        response = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response

class UpdateMemberInfoDependents(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "pages/form.html"
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


class UpdateExpenseDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Expenses
    form_class = ExpenseForm
    success_url = reverse_lazy("other_expense_page")
    template_name = "pages/form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Expense Detail"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Expense details updated successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="danger",
                )
        return response