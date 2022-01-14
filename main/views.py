import shelve
from main.models import Pokemon, Tipo, Habilidad, GrupoHuevo
from django.shortcuts import render, get_list_or_404
from main.populateDB import populateDB

def index(request): 
    return render(request,'index.html')

def populate(request):
    populateDB()
    return render(request, 'populate.html')

