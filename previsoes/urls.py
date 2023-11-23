from django.urls import path
from .  import views

urlpatterns = [
    path('resumo', views.render_graphs)
]