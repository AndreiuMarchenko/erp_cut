from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from . import views
app_name = 'sales'
urlpatterns = [
    path('unique-clients', views.UniqueView.as_view(), name='unique-all'),
    path('add-clients', views.AddClients.as_view(), name='AddClients'),
    path('get-client-info/<int:client_id>/', views.get_client_info, name='AddClients'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
