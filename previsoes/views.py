from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def render_graphs(request):
    return render(request, "graphs.html")