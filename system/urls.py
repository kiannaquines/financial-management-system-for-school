from django.urls import path
from system.views import *
from system.app_views.view import *
from system.app_views.add import *

urlpatterns = [
    path('',dashboard_page, name='dashboard'),
    path('beneficiary/list',beneficiary_page, name='beneficiary_page'),
    path('payments/list',payments_page, name='payments_page'),
    path('members/list',membership_page, name='membership_page'),
    path('users/list',users_page, name='users_page'),

    path('beneficiary/new',add_beneficiary_page, name='add_beneficiary_page'),
    path('member/new',add_member_page, name='add_member_page'),
    path('payment/new',add_payment_page, name='add_payment_page'),
    path('user/new',add_user_page, name='add_user_page'),
]
