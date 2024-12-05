from django.urls import path
from system.app_views.create_view import *
from system.app_views.remove_view import *
from system.app_views.update_view import *
from system.app_views.employee_views import *
from system.app_views.display_view import *
from authentication.views import *

urlpatterns = [
    # Dashboard
    path("", dashboard_page, name="dashboard"),

    # Auth URL's
    path("user/logout", auth_logout_page, name="auth_logout_page"),

    # Beneficiary URL's
    path("beneficiary/list", beneficiary_page, name="beneficiary_page"),
    path("beneficiary/new", add_beneficiary_page, name="add_beneficiary_page"),
    path("beneficiary/edit/<int:pk>",UpdateBeneficiaryDetails.as_view(),name="update_beneficiary"),
    path("beneficiary/delete/<int:pk>",DeleteBeneficiaryDetails.as_view(),name="delete_beneficiary"),

    # Payments URL's
    path("payments/list", payments_page, name="payments_page"),
    path("payment/new", add_payment_page, name="add_payment_page"),
    path("payments/edit/<int:pk>", UpdatePaymentDetails.as_view(), name="update_payment"),
    path("payments/delete/<int:pk>",DeletePaymentDetails.as_view(),name="delete_payment"),

    # Membership URL's
    path("members/list", membership_page, name="membership_page"),
    path("members/pending/list", pending_membership_page, name="pending_membership_page"),
    path("member/new", add_member_page, name="add_member_page"),
    path("members/edit/<int:pk>",UpdateMembershipDetails.as_view(),name="update_membership"),
    path("members/dependent/edit/<int:pk>",UpdateMemberInfoDependents.as_view(),name="update_dependent_membership"),
    path("members/delete/<int:pk>",DeleteMembershipDetails.as_view(),name="delete_membership"),
    path("membership/approve/<int:pk>", approve_membership, name="approve_membership"),
    path('member/update/info/<int:pk>', UpdateMemberInfoDependents.as_view(), name="update_membership_dependent_page"),

    #  Users URL's
    path("users/list", users_page, name="users_page"),
    path("users/inactive/list", inactive_users_page, name="inactive_users_page"),
    path("users/new", add_user_page, name="add_user_page"),
    path("users/edit/<int:pk>", UpdateUserDetails.as_view(), name="update_user"),
    path("users/edit/change_password/<int:pk>",UpdatePasswordDetails.as_view(),name="change_password"),
    path("users/activate/<int:pk>", activate_user, name="activate_user"),
    path("users/delete/<int:pk>", DeleteUserDetails.as_view(), name="delete_user"),


    # Assistance URL's
    path("assistance/list", assistance_page, name="assistance_page"),
    path("assistance/new", add_assistance_page, name="add_assistance_page"),
    path("assistance/edit/<int:pk>",UpdateAssistanceDetails.as_view(),name="update_assistance"),
    path("assistance/delete/<int:pk>",DeleteAssistanceDetails.as_view(),name="delete_assistance"),
    path("assistance/pending/list",pending_assistance_page,name="pending_assistance_page"),
    path("assistance/approve/<int:pk>", approve_assistance, name="approve_assistance"),
    path('assistance/update/release/<int:pk>', UpdateAssistanceReleaseStatusDetails.as_view(), name="update_assistance_release_status_details"),


    # Expenses 
    path("expenses/list", other_expense_page, name="other_expense_page"),
    path("expenses/add", add_expense_page, name="add_expense_page_form"),
    path("expenses/release", assistance_expense_page, name="release_expense_page"),
    path("expenses/update/<int:pk>", UpdateExpenseDetails.as_view(), name="update_expense_page_form"),
    path("expenses/delete/<int:pk>", DeleteExpenseDetails.as_view(), name="delete_expense_page_form"),
    
    # Report
    path("report/fee/generate/list", generate_annual_fee, name="generate_annual_fee"),
    path("report/fee/list", membership_fee_page, name="membership_fee_page"),
    path("report/expense/list", assistance_expense_page, name="report_expense_page"),
    path("report/monthly/dues/generate/list", generate_dues_fee, name="generate_dues_fee"),
    path("report/expense/dues/generate/list",generate_expense_fee,name="generate_expense_fee"),
    path("report/others/expense/generate/list", generate_other_expense, name="generate_other_expense"),
    path("report/monthly/dues/list", monthly_due_page, name="monthly_due_page"),
    path("report/expense/assistance/list",assistance_report_expense_page,name="assistance_report_expense_page"),
    path("report/other_expense/assistance/list",other_report_expense_page,name="other_report_expense_page"),
    
    # Ledger
    path('ledger/update/<int:pk>', UpdateTransactionToLedger.as_view(), name="update_ledger"),
    path('ledger/delete/<int:pk>', DeleteTransactionToLedger.as_view(), name="delete_ledger"),
    path('ledger/list', LedgerView.as_view(), name="ledger_list"),
    path('ledger/add', AddTransactionToLedger.as_view(), name="ledger_add"),
    path('ledger/list/export', ExportLedgerView.as_view(), name="export_ledger_list"),
    path('ledger/export', ExportLedgerView.as_view(), name="export_ledger_list"),

    # Employee
    path("employee/membership/add",employee_apply_membership,name="employee_apply_membership"),
    path("employee/beneficiary/add",employee_add_beneficiary,name="employee_add_beneficiary"),
    path("employee/assistance/add",employee_apply_assistance,name="employee_apply_assistance"),
    path("employee/beneficiary/list",employee_view_beneficiary,name="employee_view_beneficiary"),
    path("employee/dependents/list",employee_view_dependents,name="employee_view_dependents"),
    path("employee/dependents/add",add_my_dependent_page,name="add_my_dependent_page"),
    path("employee/payment/list", employee_view_payments, name="employee_view_payments"),
    path("employee/assistance/list",employee_assistance_request,name="employee_assistance_request"),
    path("employee/beneficiary/edit/<int:pk>",BeneficiaryUpdateView.as_view(),name="employee_update_beneficiary"),
    path("employee/beneficiary/delete/<int:pk>",BeneficiaryUpdateView.as_view(),name="employee_delete_beneficiary"),
    path("employee/assistance/edit/<int:pk>",AssistanceUpdateView.as_view(),name="employee_update_assistance"),
    path("employee/assistance/delete/<int:pk>",AssistanceDeleteView.as_view(),name="employee_delete_assistance"),
    path('employee/membership/me/<int:pk>', my_membership, name="membership_me"),

    # Generate Report URL's
    path("generate/report/annual/membership",generate_annual_membership_report, name="generate_annual_membership_report"),



    # Dependent
    path('dependents/list', dependents_page, name="dependents_page"),
    path('dependents/add', add_dependent_page, name="add_dependent_page"),
    path('dependents/update/<int:pk>', UpdateDependentsView.as_view(), name="update_dependent_page"),
    path('dependents/delete/<int:pk>', DeleteDependentDetails.as_view(), name="delete_dependent_page"),

    # JSON data URL's
    path("get_monthly_payment_data/",get_monthly_payment_data,name="get_monthly_payment_data"),
    path('fetch/assistance_type/count', assistance_statistics, name="assistance_type_count"),
    path('fetch/membership/count', membership_statistics, name="membership_statistics"),
]
