from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    http_method_names = ['get']
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('accounts:login')


class LoginView(BaseLoginView):
    http_method_names = ['get', 'post']
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('profiles:profile_view')
