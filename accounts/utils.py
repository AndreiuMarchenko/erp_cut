from post.models import Channels
from datetime import datetime


class DataMixin:
    title_page = None
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['previous_title'] = self.request.session.get('previous_title', 'Назва не відома')
        context['previous_url'] = self.request.META.get('HTTP_REFERER')





        context['main_channels'] = Channels.objects.filter(category_id=1).distinct()
        context['regional_channels'] = Channels.objects.filter(category_id=2).distinct()
        context['specialized_channels'] = Channels.objects.filter(category_id=4).distinct()
        context['bots'] = Channels.objects.filter(category_id=3).distinct()
        context['zakordon'] = Channels.objects.filter(category_id=5).distinct()

        
        return context

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        self.extra_context['date_header'] = datetime.now().date()
        
    

