from django.utils import timezone
from django.shortcuts import render
from system.models import *
from system.forms import *
from authentication.forms import RegistrationForm
from system.utils import oneshot_add_function
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error



@login_required(login_url="/auth/")
def add_dependent_page(request):
    path = reverse_lazy("dependents_page")

    if request.method == "POST":
        form_data = DependentForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            success(
                request,
                "You have succesfully added new expense information",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_expense_page"))

    form = DependentForm()
    context = oneshot_add_function(
        form, "Dependents", "Dependent Management", "Add Dependent",
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_expense_page(request):
    path = reverse_lazy("other_expense_page")

    if request.method == "POST":
        form_data = ExpenseForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            success(
                request,
                "You have succesfully added new expense information",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_expense_page"))

    form = ExpenseForm()
    context = oneshot_add_function(
        form, "Add Expense", "Expense Management", "Add Expense"
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_assistance_page(request):
    path = reverse_lazy("assistance_page")
    from django.db.models import F, Sum
    if request.method == "POST":
        form_data = AssistanceForm(request.POST, request.FILES)

        if form_data.is_valid():
            sum_of_collections = Payment.objects.aggregate(
                total=Sum('amount')
            )['total'] or 0

            if form_data.cleaned_data['amount'] > sum_of_collections:
                error(
                    request,
                    "Insufficient funds available for this transaction",
                    extra_tags="error_tag",
                )
                return HttpResponseRedirect(reverse_lazy("add_assistance_page"))

            form_data.save()
            success(
                request,
                "You have succesfully added new assistance information",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_assistance_page"))

    form = AssistanceForm()
    context = oneshot_add_function(
        form, "Add Assistance", "Assistance Management", "Add Assistance"
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_beneficiary_page(request):
    path = reverse_lazy("beneficiary_page")

    if request.method == "POST":
        form_data = BeneficiaryForm(request.POST, request.FILES)

        if form_data.is_valid():
            form_data.save()
            success(
                request,
                "You have successfully added new beneficiary.",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_beneficiary_page"))

    form = BeneficiaryForm()
    context = oneshot_add_function(
        form, "Add Beneficiary", "Beneficiary Management", "Add Beneficiary"
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_member_page(request):
    path = reverse_lazy("membership_page")
    if request.method == "POST":
        form_data = MembershipForm(request.POST)

        if form_data.is_valid():

            selected_beneficiaries = form_data["beneficiary"].value()

            for id in selected_beneficiaries:
                beneficiary_status = Beneficiary.objects.get(id=id)
                beneficiary_status.used = True
                beneficiary_status.save()

            form_data.save()
            success(
                request,
                "You have successfully added new membership.",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)

        else:

            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_member_page"))

    form = MembershipForm()
    context = oneshot_add_function(
        form, "Enroll Member", "Membership Management", "Enroll Member"
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_payment_page(request):
    path = reverse_lazy("payments_page")

    if request.method == "POST":
        form_data = PaymentForm(request.POST)

        if form_data.is_valid():
            paid_by_check_this_month = form_data.cleaned_data["paid_by"]
            payment_type = form_data.cleaned_data["payment_type"]

            check_query = Payment.objects.filter(
                payment_type=payment_type,
                paid_by=paid_by_check_this_month, date_paid__date=timezone.now().date()
            )
            if check_query.exists():
                success(
                    request,
                    "Employee already paid for membership this month, you can just update the payment information.",
                    extra_tags="error_tag",
                )
                return HttpResponseRedirect(path)
            
            form_data.save()
            success(
                request,
                "You have successfully added new payment.",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)
        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )
            return HttpResponseRedirect(reverse_lazy("add_payment_page"))

    form = PaymentForm()
    context = oneshot_add_function(
        form, "Add Payment", "Payment Management", "Add Payment"
    )
    return render(request, "pages/add.html", context)


@login_required(login_url="/auth/")
def add_user_page(request):
    path = reverse_lazy("users_page")
    if request.method == "POST":
        form_data = RegistrationForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            success(
                request,
                "You have successfully added new user",
                extra_tags="success_tag",
            )
            return HttpResponseRedirect(path)

        else:
            for field, errors in form_data.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )

            return HttpResponseRedirect(reverse_lazy("add_user_page"))

    form = RegistrationForm()
    context = oneshot_add_function(form, "Add User", "User Management", "Add User")
    return render(request, "pages/add.html", context)
