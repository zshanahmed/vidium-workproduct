from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Gene;
# Create your views here.

def index(request):
    genes = Gene.objects.all()
    print(genes)
    return render(request, 'vidium/index.html', context = { 'genes' : genes })

def upload(request):
    post_dict = dict(request.POST)
    print(post_dict)
    return redirect('vidium:index')