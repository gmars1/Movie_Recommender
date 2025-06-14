from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<uuid:movie_id>/', views.movie_detail, name='movie_detail'),
    path('signup/', views.signup, name='signup'),
]
