from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.http import JsonResponse
from django.core.cache import cache
from accounts.utils import DataMixin
from post.forms import *
from post.models import *
from django.views.generic import ListView, View


class Calendars(LoginRequiredMixin, DataMixin, ListView):
    models = Post
    template_name = 'calendar.html'
    title_page = 'Календар'
    context_object_name = "clients"


    MONTH_NAMES_UK = {
        1: "Січень",
        2: "Лютий",
        3: "Березень",
        4: "Квітень",
        5: "Травень",
        6: "Червень",
        7: "Липень",
        8: "Серпень",
        9: "Вересень",
        10: "Жовтень",
        11: "Листопад",
        12: "Грудень",
    }    
    def get_queryset(self):
        slug = self.kwargs['slug']
        channel = get_object_or_404(Channels, slug=slug)
        return Post.objects.filter(channel_id=channel.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
       
        slug = self.kwargs['slug']
        channel_name = Channels.objects.get(slug=slug)
        context['channel_name'] = channel_name.name
        context['title'] = self.title_page + " " + channel_name.name

        self.request.session['previous_title'] = self.title_page + " " + channel_name.name

        today = datetime.datetime.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        # Cache key for the calendar structure
        cache_key = f"calendar_structure_{year}_{month}"
        calendar_structure = cache.get(cache_key)

        if not calendar_structure:
            first_day_of_month = datetime.datetime(year, month, 1)
            first_weekday = first_day_of_month.weekday()
            start_date = first_day_of_month - timedelta(days=first_weekday)
            dates = [[(start_date + timedelta(days=i + j*7)).date() for i in range(7)] for j in range(5)]
            
            # Save the calendar structure to cache
            calendar_structure = {
                'dates': dates,
                'prev_month': datetime.datetime(year - 1, 12, 1) if month == 1 else datetime.datetime(year, month - 1, 1),
                'next_month': datetime.datetime(year + 1, 1, 1) if month == 12 else datetime.datetime(year, month + 1, 1),
                'month_name': self.MONTH_NAMES_UK[month],
                'hours': [f"{hour:02}:00" for hour in range(9, 22)]
            }
            cache.set(cache_key, calendar_structure, 60*60*24)  # Cache for one day

        context.update(calendar_structure)
        
        return context   


class CalendarDataView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        slug = kwargs['slug']

        ukrainian_months = {
            "січня": "January",
            "лютого": "February",
            "березня": "March",
            "квітня": "April",
            "травня": "May",
            "червня": "June",
            "липня": "July",
            "серпня": "August",
            "вересня": "September",
            "жовтня": "October",
            "листопада": "November",
            "грудня": "December",
        }
        
        for uk, en in ukrainian_months.items():
            date = date.replace(uk, en)
        date = date.replace(' р.', '')    
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

        # Отримання каналу
        channel = get_object_or_404(Channels, slug=slug)

        # Фільтрування постів за конкретною датою
        posts = PostChannel.objects.filter(
            channel_id=channel.id,
            date_post=date_obj
        ).annotate(
            category_name=F('post__category__name'),
            tariff=F('post__tariff'),
            slug=F('post__slug')
        ).values('date_post', 'time_post', 'tarif', 'tariff', 'category_name', 'status_write', 'slug', 'channels_slug')

        return JsonResponse(list(posts), safe=False)
