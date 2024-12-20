from typing import Any
from django.forms import BaseModelForm
from system.models import *
from system.forms import *
from authentication.forms import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView


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
            extra_tags='success'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

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
        messages.success(
            self.request,
            "Assistance details removed successfully.",
            extra_tags="success",
        )
        return form

class DeleteAssistanceDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Assistance
    success_url = reverse_lazy("assistance_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Remove Assistance Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Assistance details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to removing the assistance details",
            extra_tags="danger",
        )
        return response


class DeleteUserDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = AuthUser
    success_url = reverse_lazy("users_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Remove User Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request, "User details removed successfully.", extra_tags="success"
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to remove the user details",
            extra_tags="danger",
        )
        return response


class DeletePaymentDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Payment
    success_url = reverse_lazy("payments_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Remove Payment Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Payment removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to remove the payment details",
            extra_tags="danger",
        )
        return response


class DeleteBeneficiaryDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Beneficiary
    success_url = reverse_lazy("beneficiary_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Remove Beneficiary Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Beneficiary details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to remove the beneficiary details",
            extra_tags="danger",
        )
        return response


class DeleteMembershipDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Membership
    success_url = reverse_lazy("membership_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Removed Membership Details"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Membership details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to removed the membership details",
            extra_tags="danger",
        )
        return response


class DeleteExpenseDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Expenses
    success_url = reverse_lazy("other_expense_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Removed Expense Detail"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Expense details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to removed the expense details",
            extra_tags="danger",
        )
        return response
    

class DeleteDependentDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = Dependents
    success_url = reverse_lazy("dependents_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Removed Dependent Detail"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Dependent details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to removed the dependent details",
            extra_tags="danger",
        )
        return response
    

class RemoveSchoolYearDetails(DeleteView):
    pk_url_kwarg = "pk"
    model = SchoolYear
    success_url = reverse_lazy("school_page")
    template_name = "pages/delete.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Removed School Year Detail"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(
            self.request,
            "School year details removed successfully.",
            extra_tags="success",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        messages.error(
            self.request,
            "There is an error while trying to removed the school year details",
            extra_tags="danger",
        )
        return response