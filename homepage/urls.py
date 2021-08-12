from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   
    path('',views.index,name='home_page'),
    path('post/',views.post,name='new_post'),
     path('post-like/<int:pk>', views.postlike, name="post_like"),
     path('comment-post/<int:pk>',views.comment,name='comment_post')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
