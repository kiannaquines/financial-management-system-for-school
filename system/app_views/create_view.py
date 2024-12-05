from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from authentication.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.forms import BaseModelForm
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from typing import Any
from system.models import *
from system.forms import *

class AddSchoolYear(CreateView):
    template_name = "pages/form.html"
    model = SchoolYear
    form_class = SchoolYearForm
    success_url = reverse_lazy("school_page")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add School Year"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            "You have successfully added a new school year.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error,extra_tags="danger")
        return super().form_invalid(form)
    
class AddTransactionToLedger(CreateView):
    template_name = "pages/form.html"
    model = Ledger
    form_class = LedgerForm
    success_url = reverse_lazy("ledger_list")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Transaction"
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.recorded_by = self.request.user
        messages.success(
            self.request,
            "You have successfully added a new transaction to the ledger.",
            extra_tags="success",
        )
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


@login_required(login_url="/auth/")
def add_my_dependent_page(request):
    context = {}
    if request.method == "POST":
        form_data = MyDependentForm(request.POST)

        if form_data.is_valid():
            get_membership = Membership.objects.filter(user_id=request.user).first()
            form_data.instance.related_to_member = get_membership

            form_data.save()
            messages.success(
                request,
                "You have succesfully added new dependent information",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("employee_view_dependents"))
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_my_dependent_page"))

    form = MyDependentForm()
    context["form"] = form
    context['header_title'] = 'Add Dependent'
    return render(request, "employee/form.html", context)


@login_required(login_url="/auth/")
def add_dependent_page(request):
    context = {}

    if request.method == "POST":
        form_data = DependentForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            messages.success(
                request,
                "You have succesfully added new dependent information",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("dependents_page"))
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_expense_page"))

    form = DependentForm()
    context["form"] = form
    context["header_title"] = "Add Dependent"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_expense_page(request):
    context = {}

    if request.method == "POST":
        form_data = ExpenseForm(request.POST)

        if form_data.is_valid():

            sum_of_collections = (
                Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
            )

            if form_data.cleaned_data["amount"] > sum_of_collections:
                messages.error(
                    request,
                    "Insufficient funds available for this transaction",
                    extra_tags="info",
                )
                return HttpResponseRedirect(reverse_lazy("add_expense_page_form"))
        
            form_data.save()
            messages.success(
                request,
                "You have succesfully added new expense information",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("other_expense_page"))
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_expense_page_form"))

    form = ExpenseForm()
    context["form"] = form
    context["header_title"] = "Add Other Expense"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_assistance_page(request):
    context = {}

    if request.method == "POST":
        form_data = AssistanceForm(request.POST, request.FILES)

        if form_data.is_valid():
            sum_of_collections = (
                Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
            )

            if form_data.cleaned_data["amount_released"] > sum_of_collections:
                messages.error(
                    request,
                    "Insufficient funds available for this transaction",
                    extra_tags="info",
                )
                return HttpResponseRedirect(reverse_lazy("add_assistance_page"))

            form_data.save()
            messages.success(
                request,
                "You have succesfully added new assistance information, please wait to approve by the president of the association.",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("assistance_page"))
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_assistance_page"))

    form = AssistanceForm()
    context["form"] = form
    context["header_title"] = "Add Assistance"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_beneficiary_page(request):
    context = {}
    path = reverse_lazy("beneficiary_page")

    if request.method == "POST":
        form_data = BeneficiaryForm(request.POST, request.FILES)

        if form_data.is_valid():
            form_data.save()
            messages.success(
                request,
                "You have successfully added new beneficiary.",
                extra_tags="success",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_beneficiary_page"))

    form = BeneficiaryForm()
    context["form"] = form
    context["header_title"] = "Add Beneficiary"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_member_page(request):
    context = {}
    path = reverse_lazy("membership_page")
    if request.method == "POST":
        form_data = MembershipForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            messages.warning(
                request,
                "You have successfully added new membership. Please approve the pending membership",
                extra_tags="warning",
            )
            return HttpResponseRedirect(path)

        else:

            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_member_page"))

    form = MembershipForm()
    context["form"] = form
    context["header_title"] = "Enroll Member"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_payment_page(request):
    context = {}
    if request.method == "POST":
        form_data = PaymentForm(request.POST)

        if form_data.is_valid():
            paid_by_check_this_month = form_data.cleaned_data["paid_by"]
            payment_type = form_data.cleaned_data["payment_type"]

            check_query = Payment.objects.filter(
                payment_type=payment_type,
                paid_by=paid_by_check_this_month,
                date_paid__date=timezone.now().date(),
            )
            if check_query.exists():
                messages.success(
                    request,
                    "Employee already paid for membership this month, you can just update the payment information.",
                    extra_tags="danger",
                )
                return HttpResponseRedirect(reverse_lazy("add_payment_page"))

            form_data.save()
            messages.success(
                request,
                "You have successfully added new payment.",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("payments_page"))
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )
            return HttpResponseRedirect(reverse_lazy("add_payment_page"))

    form = PaymentForm()
    context["form"] = form
    context["header_title"] = "Add Payment"
    return render(request, "pages/form.html", context)


@login_required(login_url="/auth/")
def add_user_page(request):
    context = {}
    if request.method == "POST":
        form_data = RegistrationForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            messages.success(
                request,
                "You have successfully added new user",
                extra_tags="success",
            )
            return HttpResponseRedirect(reverse_lazy("users_page"))

        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    messages.error(
                        request,
                        err,
                        extra_tags="danger",
                    )

            return HttpResponseRedirect(reverse_lazy("add_user_page"))

    form = RegistrationForm()
    context["form"] = form
    context["header_title"] = "Create User"
    return render(request, "pages/form.html", context)
