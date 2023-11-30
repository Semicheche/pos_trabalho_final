from django.urls import path
from .  import views

urlpatterns = [
    path('overview', views.overview),
    path('detalhes', views.detalhes)
]