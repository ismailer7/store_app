from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('store_id=<int:store_id>', views.add_preffer, name='prefer'),
    path('prefferedPage/', views.favorites, name='favorite'),
    path('prefferedPage/store_id=<int:store_id>', views.remove_from_favorites, name='rfavorite'),
    path('dislike/store_id=<int:store_id>', views.dislike_store, name='block'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
