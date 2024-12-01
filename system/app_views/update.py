from typing import Any
from django.forms import BaseModelForm
from system.models import *
from system.forms import *
from authentication.forms import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.messages import success, error
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from system.mixins import CustomLoginRequiredMixin

class UpdateDependentsInfoView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    template_name = 'pages/update.html'
    model = Membership
    form_class = UpdateDependentsForm
    success_url = reverse_lazy("membership_page")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        success(
            self.request,
            "Dependent details updated successfully.",
            extra_tags="success_tag",
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
                    extra_tags="error_tag",
                )
        return super().form_invalid(form)

class UpdateDependentsView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = 'pages/update.html'
    model = Dependents
    form_class = DependentForm
    success_url = reverse_lazy("dependents_page")


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        success(
            self.request,
            "Dependent details updated successfully.",
            extra_tags="success_tag",
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
                    extra_tags="error_tag",
                )
        return super().form_invalid(form)


class UpdatePasswordDetails(CustomLoginRequiredMixin, PasswordChangeView):
    pk_url_kwarg = "pk"
    model = AuthUser
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users_page")
    template_name = "pages/update.html"

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
                    extra_tags="error_tag",
                )
        return super().form_invalid(form)


class UpdateAssistanceDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Assistance
    form_class = AssistanceForm
    success_url = reverse_lazy("assistance_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Assistance Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response


class UpdateUserDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = AuthUser
    form_class = AdminRegistrationForm
    success_url = reverse_lazy("users_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update User Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request, "User details updated successfully.", extra_tags="success_tag"
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response


class UpdatePaymentDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy("payments_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Payment Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Payment details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response


class UpdateBeneficiaryDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Beneficiary
    form_class = BeneficiaryForm
    success_url = reverse_lazy("beneficiary_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Beneficiary Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Beneficiary details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response


class UpdateMembershipDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy("membership_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Membership Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Membership details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response




class UpdateAssistanceReleaseStatusDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Assistance
    form_class = AssistanceReleaseStatusForm
    success_url = reverse_lazy("assistance_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Assistance Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Assistance details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response

class UpdateExpenseDetails(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    model = Expenses
    form_class = ExpenseForm
    success_url = reverse_lazy("other_expense_page")
    template_name = "pages/update.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Update Expense Detail"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        success(
            self.request,
            "Expense details updated successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for err in errors:
                error(
                    self.request,
                    f"{err}",
                    extra_tags="error_tag",
                )
        return response