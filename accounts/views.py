from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .utils import *

class Login(LoginView):
    form_class = UserAuth
    template_name = 'login.html'
    title_page = 'Авторизація'


class dashboard(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "dashboard.html"
    title_page = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['previous_title'] = self.title_page 

        return context

