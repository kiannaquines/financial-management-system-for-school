from django.shortcuts import render
from authentication.forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect

def auth_index_page(request):
    context = {}
    form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('dashboard'))
            else:
                print(login_form.errors)
                
    context['form'] = form
    return render(request, 'login.html',context)

def auth_register_page(request):
    context = {}
    form = UserRegistrationForm()

    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect(reverse_lazy('login'))
        else:
            print(register_form.errors)

    context['form'] = form
    return render(request, 'register.html',context)


def auth_logout_page(request):
    logout(request)
    return HttpResponseRedirect('/auth/')