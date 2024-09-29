from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class CustomLoginRequiredMixin(AccessMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = "You must be logged in to access this page."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message, extra_tags='error_tag')
        return redirect(self.login_url)