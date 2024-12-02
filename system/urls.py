from django.urls import path
from system.views import *
from system.app_views.view import *
from system.app_views.add import *
from authentication.views import auth_logout_page
from system.app_views.update import *
from system.app_views.delete import *
from system.app_views.employee_views import *

urlpatterns = [
    path("", dashboard_page, name="dashboard"),
    path("beneficiary/list", beneficiary_page, name="beneficiary_page"),
    path("payments/list", payments_page, name="payments_page"),
    path("members/list", membership_page, name="membership_page"),
    path("members/pending/list", pending_membership_page, name="pending_membership_page"),
    path("users/list", users_page, name="users_page"),
    path("users/inactive/list", inactive_users_page, name="inactive_users_page"),
    path("assistance/list", assistance_page, name="assistance_page"),

    path("expenses/release", assistance_expense_page, name="release_expense_page"),
    path("expenses/list", other_expense_page, name="other_expense_page"),
    path("expenses/add", add_expense_page, name="add_expense_page_form"),
    path("expenses/update/<int:pk>", UpdateExpenseDetails.as_view(), name="update_expense_page_form"),
    path("expenses/delete/<int:pk>", DeleteExpenseDetails.as_view(), name="delete_expense_page_form"),

    path("assistance/pending/list",pending_assistance_page,name="pending_assistance_page"),
    path("beneficiary/new", add_beneficiary_page, name="add_beneficiary_page"),
    path("member/new", add_member_page, name="add_member_page"),
    path("payment/new", add_payment_page, name="add_payment_page"),
    path("user/new", add_user_page, name="add_user_page"),
    path("assistance/new", add_assistance_page, name="add_assistance_page"),
    path("user/logout", auth_logout_page, name="auth_logout_page"),
    
    # Update Route
    path("members/edit/<int:pk>",UpdateMembershipDetails.as_view(),name="update_membership"),
    path("members/dependent/edit/<int:pk>",UpdateMemberInfoDependents.as_view(),name="update_dependent_membership"),
    path("beneficiary/edit/<int:pk>",UpdateBeneficiaryDetails.as_view(),name="update_beneficiary"),
    path("payments/edit/<int:pk>", UpdatePaymentDetails.as_view(), name="update_payment"),
    path("users/edit/<int:pk>", UpdateUserDetails.as_view(), name="update_user"),
    path("assistance/edit/<int:pk>",UpdateAssistanceDetails.as_view(),name="update_assistance"),
    path("users/edit/change_password/<int:pk>",UpdatePasswordDetails.as_view(),name="change_password"),

    # Delete Route
    path("members/delete/<int:pk>",DeleteMembershipDetails.as_view(),name="delete_membership"),
    path("beneficiary/delete/<int:pk>",DeleteBeneficiaryDetails.as_view(),name="delete_beneficiary"),
    path("payments/delete/<int:pk>",DeletePaymentDetails.as_view(),name="delete_payment"),
    path("users/delete/<int:pk>", DeleteUserDetails.as_view(), name="delete_user"),
    path("assistance/delete/<int:pk>",DeleteAssistanceDetails.as_view(),name="delete_assistance"),
    path("report/fee/list", membership_fee_page, name="membership_fee_page"),
    path("report/monthly/dues/list", monthly_due_page, name="monthly_due_page"),
    path("report/expense/list", assistance_expense_page, name="report_expense_page"),

    # Generate Report Route assistance_report_expense_page
    path("report/fee/generate/list", generate_annual_fee, name="generate_annual_fee"),
    path("report/monthly/dues/generate/list", generate_dues_fee, name="generate_dues_fee"),
    path("report/expense/dues/generate/list",generate_expense_fee,name="generate_expense_fee"),

    # Other and Assistance Expense
    path("report/others/expense/generate/list", generate_other_expense, name="generate_other_expense"),


    path("report/expense/assistance/list",assistance_report_expense_page,name="assistance_report_expense_page"),
    path("report/other_expense/assistance/list",other_report_expense_page,name="other_report_expense_page"),


    # Approve
    path("assistance/approve/<int:pk>", approve_assistance, name="approve_assistance"),
    path("membership/approve/<int:pk>", approve_membership, name="approve_membership"),
    path("user/activate/<int:pk>", activate_user, name="activate_user"),

    # Employee Routes
    path("employee/membership/add",employee_apply_membership,name="employee_apply_membership"),
    path("employee/beneficiary/add",employee_add_beneficiary,name="employee_add_beneficiary"),
    path("employee/assistance/add",employee_apply_assistance,name="employee_apply_assistance"),
    path("employee/beneficiary/list",employee_view_beneficiary,name="employee_view_beneficiary"),
    path("employee/payment/list", employee_view_payments, name="employee_view_payments"),
    path("employee/assistance/list",employee_assistance_request,name="employee_assistance_request"),
    path("employee/beneficiary/edit/<int:pk>",BeneficiaryUpdateView.as_view(),name="employee_update_beneficiary"),
    path("employee/beneficiary/delete/<int:pk>",BeneficiaryDeleteView.as_view(),name="employee_delete_beneficiary"),
    path("employee/assistance/edit/<int:pk>",AssistanceUpdateView.as_view(),name="employee_update_assistance"),
    path("employee/assistance/delete/<int:pk>",AssistanceDeleteView.as_view(),name="employee_delete_assistance"),
    path("generate/report/annual/membership",generate_annual_membership_report, name="generate_annual_membership_report"),
    path("get_monthly_payment_data/",get_monthly_payment_data,name="get_monthly_payment_data"),
    path('membership/me/<int:pk>', my_membership, name="membership_me"),
    path('assistance/update/release/<int:pk>', UpdateAssistanceReleaseStatusDetails.as_view(), name="update_assistance_release_status_details"),
    path('fetch/assistance_type/count', assistance_statistics, name="assistance_type_count"),
    path('fetch/membership/count', membership_statistics, name="membership_statistics"),


    # Dependent

    path('dependents/list', dependents_page, name="dependents_page"),
    path('dependents/add', add_dependent_page, name="add_dependent_page"),
    path('dependents/update/<int:pk>', UpdateDependentsView.as_view(), name="update_dependent_page"),
    path('dependents/delete/<int:pk>', DeleteDependentDetails.as_view(), name="delete_dependent_page"),



    path('member/update/info/<int:pk>', UpdateMemberInfoDependents.as_view(), name="update_membership_dependent_page"),
    path('ledger/list', LedgerView.as_view(), name="ledger_list"),
    path('ledger/list/export', ExportLedgerView.as_view(), name="export_ledger_list"),
]
