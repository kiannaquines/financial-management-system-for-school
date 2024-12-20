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

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["user_name"],
                password=login_form.cleaned_data["password"],
            )
            
            if user is not None:
                login(request, user)

                if user.user_type == "Treasurer" or user.user_type == "President":
                    return redirect(reverse_lazy("dashboard"))
                else:
                    return redirect(reverse_lazy("employee_assistance_request"))
            else:
                error(request, "Incorrect combination of username & password, or your account still inactive please wait to active by the staff.", extra_tags="error_tag")

    context["form"] = form
    return render(request, "login.html", context)


def auth_register_page(request):
    context = {}
    form = UserRegistrationForm()

    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)

        if register_form.is_valid():
            registration = register_form.save(commit=False)
            registration.is_active = False
            registration.user_type = "Employee"
            registration.save()
            success(
                request,
                "You have successfully registered your account.",
                extra_tags="success_tag",
            )
            return redirect(reverse_lazy("login"))
        else:
            for field, errors in register_form.errors.items():
                for err in errors:
                    error(
                        request,
                        f"{err}",
                        extra_tags="error_tag",
                    )

    context["form"] = form
    return render(request, "register.html", context)


def auth_logout_page(request):
    logout(request)
    success(request, "You have successfully logout.", extra_tags="success_tag")
    return HttpResponseRedirect("/auth/")
