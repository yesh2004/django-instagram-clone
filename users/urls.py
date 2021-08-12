from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
path('register/',views.register,name='register_page'),
path('login/',views.login,name='login_page'),
path('logout/',views.logout,name='logout_page'),
path('profile/',views.profile,name='profile_page'),
path('direct/<username>',views.direct,name='direct_message'),
path('send/', views.SendDirect, name='send_direct'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
