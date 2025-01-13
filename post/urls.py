from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
app_name = 'posts'
urlpatterns = [
    path('to-buy/<slug:slug>', views.AddPostView.as_view(), name='toBuy'),
    path('arkhiv-posts/', views.ArkhivPosts.as_view(), name='arkhiv_posts'),
    path('delete-posts/<slug:slug>/<slug:channel>/', views.deletPost, name='delete_posts'),
    path('detail_post/<slug:slug>/<int:id>/', views.DetailPost.as_view(), name='detailPost'),
    path('editor/<slug:slug>/<int:post_channel_id>/', views.EditorPostView.as_view(), name='editor'),

    


    path('update-posts/<slug:slug>/', views.UpdatePostView.as_view(), name='update_posts'),
    
    path('check-time/', views.check_time, name='check_time'),
    path('view-invoice/<slug:slug>/', views.InvoiceView.as_view(), name='view_invoice'),
    path('channels/', views.ChannelsListView.as_view(), name='channels'),

    path('delete-channels/<int:channel_id>', views.DeleteChannel, name='deleteChannels'),
    path('change-channels/<int:channel_id>', views.ChangeChannel, name='changeChannels'),
    path('add-channels/', views.AddChannel, name='addChannels'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

