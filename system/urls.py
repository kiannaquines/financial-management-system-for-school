from django.urls import path
from system.views import *
from system.app_views.view import *
from system.app_views.add import *
from authentication.views import auth_logout_page
from system.app_views.update import *

urlpatterns = [
    path('',dashboard_page, name='dashboard'),
    path('beneficiary/list',beneficiary_page, name='beneficiary_page'),
    path('payments/list',payments_page, name='payments_page'),
    path('members/list',membership_page, name='membership_page'),
    path('members/pending/list', pending_membership_page, name="pending_membership_page"),
    path('users/list',users_page, name='users_page'),
    path('users/inactive/list',inactive_users_page, name='inactive_users_page'),
    path('assistance/list',assistance_page, name='assistance_page'),
    path('assistance/pending/list',pending_assistance_page, name='pending_assistance_page'),

    path('beneficiary/new',add_beneficiary_page, name='add_beneficiary_page'),
    path('member/new',add_member_page, name='add_member_page'),
    path('payment/new',add_payment_page, name='add_payment_page'),
    path('user/new',add_user_page, name='add_user_page'),
    path('assistance/new',add_assistance_page, name='add_assistance_page'),

    path('user/logout',auth_logout_page, name='auth_logout_page'),


    # Update Route
    path('members/edit/<int:pk>', UpdateMembershipDetails.as_view(), name="update_membership"),
    path('beneficiary/edit/<int:pk>', UpdateBeneficiaryDetails.as_view(), name="update_beneficiary"),
    path('payments/edit/<int:pk>', UpdatePaymentDetails.as_view(), name="update_payment"),
    path('users/edit/<int:pk>', UpdateUserDetails.as_view(), name="update_user"),
    path('assistance/edit/<int:pk>', UpdateAssistanceDetails.as_view(), name="update_assistance"),
]
