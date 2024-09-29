from django.shortcuts import render
from authentication.forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages import success, error

def auth_index_page(request):
    context = {}
    form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['user_name'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('dashboard'))
            else:
                error(request,'Invalid username or password.', extra_tags='error_tag')
                
    context['form'] = form
    return render(request, 'login.html',context)

def auth_register_page(request):
    context = {}
    form = UserRegistrationForm()

    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)

        if register_form.is_valid():
            registration = register_form.save(commit=False)
            registration.is_active = True
            registration.user_type = 'Employee'
            registration.save()
            success(request,'You have successfully registered your account.', extra_tags='success_tag')
            return redirect(reverse_lazy('login'))
        else:
            error(request,'There is something wrong with your registration, try again.', extra_tags='error_tag')

    context['form'] = form
    return render(request, 'register.html',context)


def auth_logout_page(request):
    logout(request)
    success(request,'You have successfully logout.', extra_tags='success_tag')
    return HttpResponseRedirect('/auth/')