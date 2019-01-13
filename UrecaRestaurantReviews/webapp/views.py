from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('webapp/index.html')
    return HttpResponse(template.render())

def search(request):
    template = loader.get_template('webapp/search.html')
    return HttpResponse(template.render())

def loc(request):
    template = loader.get_template('webapp/foodplace.html')
    return HttpResponse(template.render())