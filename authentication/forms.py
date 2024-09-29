from django import forms
from authentication.models import AuthUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm

class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = 'Username'
        self.fields["first_name"].label = 'Firstname'
        self.fields["last_name"].label = 'Lastname'

        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "class": "form-control"}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Password", "class": "form-control"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password", "class": "form-control"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )

    class Meta:
        model = AuthUser
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "class": "form-control"}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Password", "class": "form-control"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password", "class": "form-control"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Email", "class": "form-control"}
        )

        self.fields["user_type"].widget.attrs.update(
            {"placeholder": "User Type", "class": "form-control"}
        )

        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})

        self.fields["is_staff"].widget.attrs.update({"class": "form-check-input"})

        self.fields["is_superuser"].widget.attrs.update({"class": "form-check-input"})

    class Meta:
        model = AuthUser
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class PasswordChangeForm(BasePasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update(
            {"placeholder": "Old Password", "class": "form-control"}
        )
        self.fields["new_password1"].widget.attrs.update(
            {"placeholder": "New Password", "class": "form-control"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"placeholder": "Confirm New Password", "class": "form-control"}
        )

    class Meta:
        model = AuthUser
        fields = [
            "new_password1",
            "new_password2",
        ]


class AdminRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "class": "form-control"}
        )

        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )

        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Email", "class": "form-control"}
        )

        self.fields["user_type"].widget.attrs.update(
            {"placeholder": "User Type", "class": "form-control"}
        )

        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})

        self.fields["is_staff"].widget.attrs.update({"class": "form-check-input"})

        self.fields["is_superuser"].widget.attrs.update({"class": "form-check-input"})

    class Meta:
        model = AuthUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["user_name"].label = 'Username'
        self.fields["password"].label = 'Password'

    user_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username","class":"form-control"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password","class":"form-control"})
    )
