import shelve

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser

from main.forms import ColorForm, InicialForm
from main.models import Pokemon
from django.shortcuts import render, get_list_or_404, get_object_or_404
from main.populateDB import populateDB
from main.recommendations import topMatches


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
            #Aquí va consulta de woosh
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                myquery = QueryParser("color", ix.schema).parse(color)
                pokemons = searcher.search(myquery, limit=20)
                return render(request,'listaPokemonColor.html',{'pokemons': pokemons,'color':color})
    form = ColorForm()
    return render(request,'buscar_color.html', {'form': form})

def buscarPokemonStatsSimilares(request):
    if request.method=='GET':
        form = InicialForm(request.GET, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['pokemon_inicial']
            #Aquí va la función de las distancias entre stats
            pokemom = get_object_or_404(Pokemon, nombre=nombre)
            results = topMatches(pokemom, n=3)
            pokemons = list()
            for result in results:
                pokemons.append(result[1])
            print(str(pokemons))
            return render(request,'listaStatsParecidos.html', {'pokemons':pokemons})
    form = InicialForm()
    return render(request,'pokemon_inicial.html', {'form': form})




