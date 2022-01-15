import shelve

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser

from main.forms import ColorForm
from main.models import Pokemon
from django.shortcuts import render, get_list_or_404
from main.populateDB import populateDB

def index(request): 
    return render(request,'index.html')

def populate(request):
    populateDB()
    return render(request, 'populate.html')

def listaPokemon(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'listaPokemon.html',{'pokemons':pokemons})

def buscarPokemonPorColor(request):
    if request.method=='GET':
        form = ColorForm(request.GET, request.FILES)
        if form.is_valid():
            color = form.cleaned_data['colores']
            print("------------------------------------------------------------"+color)
            #Aquí va consulta de woosh
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                myquery = QueryParser("color", ix.schema).parse(color)
                pokemons = searcher.search(myquery)
                return render(request,'listaPokemonColor.html',{'pokemons': pokemons,'color':color})
    form = ColorForm()
    return render(request,'buscar_color.html', {'form': form})




