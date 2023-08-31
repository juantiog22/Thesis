from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
)


class PanelHomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"
    login_url = reverse_lazy('usuarios_app:user-login')
