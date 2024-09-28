from django.shortcuts import render
from system.models import *
from system.utils import oneshot_view_function
from django.urls import reverse_lazy

def beneficiary_page(request):
    path = reverse_lazy('add_beneficiary_page')
    header_list = ['First Name', 'Middle Name', 'Last Name', 'Suffix', 'Relationship', 'Date of Birth']
    field_list = ['beneficiary_first_name', 'beneficiary_middle_name', 'beneficiary_last_name', 'suffix', 'relationship', 'date_of_birth']
    context = oneshot_view_function(Beneficiary, 'Beneficiary', 'Beneficiaries List', 'Add Beneficiary', path, header_list, field_list)
    return render(request, 'pages/view.html',context)

def payments_page(request):
    path = reverse_lazy('add_payment_page')
    header_list = ['Paid By', 'Amount', 'Payment Type', 'Date Paid']
    field_list = ['paid_by__username', 'amount', 'payment_type', 'date_paid',]
    context = oneshot_view_function(Payment, 'Payment', 'Payments List', 'Add Payment', path, header_list, field_list)

    return render(request, 'pages/view.html',context)

def users_page(request):
    path = reverse_lazy('add_user_page')
    header_list = ['Username', 'Firstname', 'Lastname', 'Email', 'User Type']
    field_list = ['username', 'first_name', 'last_name', 'email', 'user_type']
    context = oneshot_view_function(AuthUser, 'User', 'Users List', 'Add User', path, header_list, field_list)
    return render(request, 'pages/view.html',context)

def membership_page(request):
    path = reverse_lazy('add_member_page')
    header_list = ['Firstname', 'Middlename', 'Lastname', 'Contact Number', 'Employee ID']
    field_list = ['first_name','middle_name', 'last_name', 'contact_number', 'employee_id']
    context = oneshot_view_function(Membership,'Membership', 'Memberships List', 'Add Member', path, header_list, field_list)
    return render(request, 'pages/view.html',context)