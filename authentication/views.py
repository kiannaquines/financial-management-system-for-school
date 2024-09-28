from django.shortcuts import render
from authentication.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def auth_index_page(request):
    context = {}
    form = LoginForm()

    if request.method == 'POST':
        pass
    
    context['form'] = form
    return render(request, 'login.html',context)

def auth_register_page(request):
    context = {}
    form = RegistrationForm()

    if request.method == 'POST':
        pass

    context['form'] = form
    return render(request, 'register.html',context)


def auth_logout_page(request):
    logout(request)
    return HttpResponseRedirect('/auth/')