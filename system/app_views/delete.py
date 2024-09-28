from typing import Any
from django.forms import BaseModelForm
from system.models import *
from system.forms import *
from authentication.forms import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.messages import success, error
from django.views.generic import DeleteView


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
        success(
            self.request,
            "Assistance details removed successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        error(
            self.request,
            "There is an error while trying to removing the assistance details",
            extra_tags="error_tag",
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
        success(
            self.request, "User details removed successfully.", extra_tags="success_tag"
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        error(
            self.request,
            "There is an error while trying to remove the user details",
            extra_tags="error_tag",
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
        success(
            self.request,
            "Payment removed successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        error(
            self.request,
            "There is an error while trying to remove the payment details",
            extra_tags="error_tag",
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
        success(
            self.request,
            "Beneficiary details removed successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        error(
            self.request,
            "There is an error while trying to remove the beneficiary details",
            extra_tags="error_tag",
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
        success(
            self.request,
            "Membership details removed successfully.",
            extra_tags="success_tag",
        )
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_invalid(form)
        error(
            self.request,
            "There is an error while trying to removed the membership details",
            extra_tags="error_tag",
        )
        return response
