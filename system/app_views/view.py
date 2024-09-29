from django.shortcuts import render
from system.models import *
from system.utils import oneshot_view_function
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/')
def beneficiary_page(request):
    path = reverse_lazy("add_beneficiary_page")
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
    context = oneshot_view_function(
        Beneficiary.objects.values(*field_list),
        "Beneficiary",
        "Beneficiaries List",
        "Add Beneficiary",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def payments_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__username",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.values(*field_list),
        "Payment",
        "Payments List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def users_page(request):
    path = reverse_lazy("add_user_page")
    header_list = ["Username", "Firstname", "Lastname", "Email", "User Type"]
    field_list = ["id", "username", "first_name", "last_name", "email", "user_type"]
    context = oneshot_view_function(
        AuthUser.objects.filter(is_active=True).values(*field_list),
        "User",
        "Users List",
        "Add User",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def inactive_users_page(request):
    path = reverse_lazy("add_user_page")
    header_list = ["Username", "Firstname", "Lastname", "Email", "User Type", "Active"]
    field_list = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "user_type",
        "is_active",
    ]
    context = oneshot_view_function(
        AuthUser.objects.filter(is_active=False).values(*field_list),
        "Inactive Users",
        "Users List",
        "Add User",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def membership_page(request):
    path = reverse_lazy("add_member_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Contact Number",
        "Employee ID",
    ]
    field_list = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "contact_number",
        "employee_id",
    ]
    context = oneshot_view_function(
        Membership.objects.filter(membership_status=True).values(*field_list),
        "Membership",
        "Memberships List",
        "Add Member",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def pending_membership_page(request):
    path = reverse_lazy("add_member_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Contact Number",
        "Employee ID",
    ]
    field_list = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "contact_number",
        "employee_id",
    ]
    context = oneshot_view_function(
        Membership.objects.filter(membership_status=False).values(*field_list),
        "Pending Membership",
        "Pending Memberships List",
        "Add Member",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=True).values(*field_list),
        "Assistance",
        "Assistance List",
        "Add Assistance",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def pending_assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=False).values(*field_list),
        "Pending Assistance",
        "Pending Assistance List",
        "Add Assistance",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.filter(assistance_status=True).values(*field_list),
        "Assistance",
        "Assistance List",
        "Add Assistance",
        path,
        header_list,
    )
    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def membership_fee_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__username",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.filter(payment_type="Membership").values(*field_list),
        "Membership Fee",
        "Membership Fee List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def monthly_due_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__username",
        "amount",
        "payment_type",
        "date_paid",
    ]
    context = oneshot_view_function(
        Payment.objects.filter(
            Q(payment_type="Delegation Pay")
            | Q(payment_type="Trust Fund")
            | Q(payment_type="Visitors Fund")
        ).values(*field_list),
        "Monthly Due",
        "Monthly Due List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)

@login_required(login_url='/auth/')
def expense_page(request):
    path = reverse_lazy("add_payment_page")
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname", "Assistance Type", "Status"]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "assistance_status",
    ]
    context = oneshot_view_function(
        Assistance.objects.values(*field_list),
        "Expense",
        "Expense List",
        "Add Payment",
        path,
        header_list,
    )

    return render(request, "pages/view.html", context)
