from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import make_aware
from django.http import JsonResponse
from django.db.models import Min, Max
from post.models import PostChannel
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from sales.forms import *
from accounts.utils import DataMixin
from sales.models import *
from datetime import datetime

class UniqueView(LoginRequiredMixin, DataMixin, ListView):
    model = Clients
    template_name = "client-to-buy.html"
    context_object_name = "clients"
    title_page = "Унікальні клієнти"
    paginate_by = 500

    def get_queryset(self):
        queryset = Clients.objects.filter(
            where="Унікальний клієнт")

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        self.request.session['previous_title'] = self.title_page 
        return context


class AddClients(LoginRequiredMixin, DataMixin, CreateView):
    model = Clients
    form_class = AddClientsForms
    template_name = 'add_user.html'
    success_url = reverse_lazy('sales:unique-all') 
    title_page = 'Додати нового клієнта'

    def get_form_kwargs(self):
        # Передаємо користувача у форму через kwargs
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form): 
        self.object = form.save(commit=False)
        published_at = datetime.now().strftime("%d-%m-%Y")

        form.instance.date = make_aware(datetime.strptime(published_at, "%d-%m-%Y"))
        form.instance.where = "Унікальний клієнт"

        form.instance.sales_manager = self.request.user
        self.object.save()
        return super().form_valid(form)  
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['previous_title'] = self.title_page 
        context['btn_name'] = 'Додати клієнта'
        return context





def get_client_info(request, client_id):
    client = get_object_or_404(Clients, pk=client_id)
    sales_data = PostChannel.objects.filter(
        post__username=client.social_media).aggregate(
        first_purchase=Min('date_post'),
        last_purchase=Max('date_post')
    )

    data = {
        "id": client.id,
        "social_media": client.social_media if client.social_media else "Дані відсутні",
        "data": client.date if client.date else "Дані відсутні",
        "link": client.link if client.link else "Дані відсутні",
        "data_the_first_buys": sales_data['first_purchase'] if sales_data['first_purchase'] else "Дані не знайдено",
        "data_the_last_buys": sales_data['last_purchase'] if sales_data['last_purchase'] else "Дані не знайдено",
        "client_cost": PostChannel.objects.filter(post__username=client.social_media).count(),
        "city": client.city if client.city else "Дані відсутні",
        "slug": client.slug if client.slug else "Дані відсутні",
    }

    return JsonResponse(data)

