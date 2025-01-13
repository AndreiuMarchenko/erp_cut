from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('sales.urls')),
    path('', include('post.urls')),
    path('', include('calendarForPosts.urls')),
]



