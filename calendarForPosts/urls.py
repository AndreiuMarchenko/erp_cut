from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from . import views
app_name = 'calendars'
urlpatterns = [
    path('calendar/<slug:slug>', views.Calendars.as_view(), name='calendar'),
    path('calendar-data/<slug:slug>/', views.CalendarDataView.as_view(), name='calendar_data'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
