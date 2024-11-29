from django.http import HttpResponse
from django.shortcuts import render
from system.models import *
from system.utils import oneshot_view_function
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/")
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


@login_required(login_url="/auth/")
def payments_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
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


@login_required(login_url="/auth/")
def users_page(request):
    path = reverse_lazy("add_user_page")
    header_list = ["Username", "Firstname", "Lastname", "Email", "Type"]
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


@login_required(login_url="/auth/")
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


@login_required(login_url="/auth/")
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


@login_required(login_url="/auth/")
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


@login_required(login_url="/auth/")
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = ["Firstname", "Middlename", "Lastname","Assistance Type", "Status"]
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


@login_required(login_url="/auth/")
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


@login_required(login_url="/auth/")
def assistance_page(request):
    path = reverse_lazy("add_assistance_page")
    header_list = [
        "Firstname",
        "Middlename",
        "Lastname",
        "Assistance Type",
        "Amount Released",
        "Release Status",
        "Status",
    ]
    field_list = [
        "id",
        "assistance_first_name",
        "assistance_middle_name",
        "assistance_last_name",
        "type_of_assistance",
        "amount_released",
        "released_status",
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


@login_required(login_url="/auth/")
def membership_fee_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
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
    context["schools"] = [school[0] for school in Membership.SCHOOL_AFFILIATION]
    return render(request, "pages/view.html", context)


@login_required(login_url="/auth/")
def monthly_due_page(request):
    path = reverse_lazy("add_payment_page")
    header_list = ["Paid By", "Amount", "Payment Type", "Date Paid"]
    field_list = [
        "id",
        "paid_by__user_id__first_name",
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


@login_required(login_url="/auth/")
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


def is_exactly_11_months(start_date, end_date):
    months_difference = (end_date.year - start_date.year) * 11 + (
        end_date.month - start_date.month
    )
    print(months_difference)
    return months_difference == 11


from datetime import datetime, timedelta
from django.utils import timezone
from calendar import monthrange
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/")
def generate_annual_membership_report(request):
    if request.method == "POST":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="annual_membership_payment.pdf"'
        )

        school_year_from = request.POST.get("range_from")
        school_year_to = request.POST.get("range_to")
        school = request.POST.get("school")

        start_date = timezone.make_aware(
            datetime.strptime(school_year_from, "%Y-%m-%d")
        )
        end_date = timezone.make_aware(datetime.strptime(school_year_to, "%Y-%m-%d"))

        if not is_exactly_11_months(start_date, end_date):
            messages.warning(
                request,
                "The selected date range is incorrect, please try again.",
                extra_tags="error_tag",
            )
            return redirect(reverse_lazy("membership_fee_page"))

        month_headers = []
        current_date = start_date
        while current_date <= end_date:
            month_headers.append(current_date.strftime("%m"))
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(
                day=1
            )

        payments = Payment.objects.filter(
            date_paid__range=(start_date, end_date),
            payment_type="Membership",
        )

        if school and school != "All":
            payments = payments.filter(paid_by__school_affiliation=school)

        if not payments.exists():
            messages.warning(
                request,
                "No membership payment found using the provided date range and school, please try again later.",
                extra_tags="error_tag",
            )
            return redirect(reverse_lazy("membership_fee_page"))

        member_result = []
        total_paid_amount = 0

        for payment in payments:
            fullname = f"{payment.paid_by.last_name}, {payment.paid_by.first_name}"
            monthly_payments = {month: 0 for month in month_headers}
            current_date = start_date
            member_total_paid = 0

            while current_date <= end_date:
                month_start = current_date.replace(day=1)
                last_day = monthrange(current_date.year, current_date.month)[1]
                month_end = current_date.replace(day=last_day)

                month_payments = Payment.objects.filter(
                    date_paid__range=(month_start, month_end),
                    payment_type="Membership",
                    paid_by=payment.paid_by,
                )

                total_paid = month_payments.aggregate(total=Sum("amount"))["total"] or 0
                monthly_payments[current_date.strftime("%m")] = f'{int(total_paid):,}'
                member_total_paid += int(total_paid)
                current_date += timedelta(days=last_day)

            member_result.append(
                {
                    "fullname": fullname,
                    "monthly_payments": monthly_payments,
                    "total_paid": f'{int(member_total_paid):,}',
                }
            )

            total_paid_amount += member_total_paid

        context = {
            "school": school,
            "month_headers": month_headers,
            "member_result": member_result,
            "school_year": f"SCHOOL YEAR {start_date.year} - {end_date.year}",
            "total_amount": f"{total_paid_amount:,}",
            "report_date": timezone.now().strftime("%B %d, %Y"),
            "prepared_by": f'{request.user.first_name} {request.user.last_name}',
            "report_type": f'Annual Membership Report',
        }

        template = get_template("membership_report.html")
        html = template.render(context)
        pisa.CreatePDF(html, dest=response)

        return response
