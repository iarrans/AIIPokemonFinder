#encoding:utf-8
from main.models import Pokemon, Tipo, Habilidad, GrupoHuevo

from bs4 import BeautifulSoup
import urllib.request
#import lxml
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, ID
#from whoosh.qparser import QueryParser
#from whoosh.qparser import MultifieldParser
import csv
import os, ssl,shutil

#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    
    #borramos todas las tablas de la BD
    Pokemon.objects.all().delete()
    Tipo.objects.all().delete()
    Habilidad.objects.all().delete()
    GrupoHuevo.objects.all().delete()
    pokemons = {}
    types = {}
    abilities = {}
    egggroups = {}
    # eliminamos el directorio del indice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    # creamos indice
    ix = create_in("Index", schema=get_schema())
    # creamos un writer para poder aÃ±adir documentos al indice
    writer = ix.writer()
    i = 0
    
    #extraemos los datos de la web con BS, con datos del csv
    with open('main/pokemon.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for pokemon in csvreader:
            numpokedex = int(pokemon[0])
            nombre = pokemon[1]
            generacion = int(pokemon[11])
            if (not "Mega " in nombre):
                # construimos enlaces
                wikidex = urllib.request.urlopen("https://www.wikidex.net/wiki/" + nombre)
                pokexpertoaux = urllib.request.urlopen(
                    "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk=" + str(numpokedex))
                veekunaux = urllib.request.urlopen("https://veekun.com/dex/pokemon/" + nombre)
                # -------------------------------------------------------scrapping wikidex
                wikidex2 = BeautifulSoup(wikidex, "lxml", from_encoding='utf8')
                datos = wikidex2.find("div", class_="ctipo").find("table", class_="datos resalto").find_all("td")
                if len(datos) == 15:
                    # pueden tener más de una habilidad
                    # SCRAPPING DE HABILIDAD
                    habilidad2 = datos[3].get_text(separator=";").strip()
                    x = habilidad2.split(";")
                    if len(x) > 1:
                        y = []
                        y.append(x[0])
                        if x[1] == "":
                            x[1] = "no aplica"
                        else:
                            y.append(x[1])
                        habilidades = y
                    else:
                        habilidades = [habilidad2]
                    # SCRAPPING DE HABITAT
                    habitat = datos[9].text.strip()
                    # SCRAPPING DE COLOR
                    color = datos[10].text.strip()
                    # SCRAPPING DE GRUPO HUEVO
                    # pueden tener más de un grupo huevo
                    ghuevo = datos[7].get_text(separator=":").strip()
                    a = ghuevo.split(":")
                    if len(a) > 1:
                        b = []
                        for grupo in a:
                            b.append(grupo)
                        ghuevo = b
                    else:
                        ghuevo = [ghuevo]
                    # -------------------------------------------------------scrapping pokexperto
                    pokexperto = BeautifulSoup(pokexpertoaux, "lxml", from_encoding='utf8')
                    # SCRAPPING DE IMAGEN
                    imagen = pokexperto.find("td", class_="center bordedcho").find_all("img")
                    imagen1 = imagen[0]['src']
                    imagenurl = 'https://www.pokexperto.net/' + imagen1

                    # SCRAPPING DE TIPOS
                    datosbasicos = pokexperto.find("td", class_="bordeambos").find_all("td")
                    tipos = datosbasicos[1].find_all("img")
                    tipo1 = tipos[0]['alt']
                    if len(tipos) > 1:
                        tipo2 = tipos[1]['alt']
                        tipospk = [tipo1, tipo2]
                    else:
                        tipospk = [tipo1]
                    # -------------------------------------------------------scrapping veekun
                    # SCRAPPING DE STATS
                    veekun = BeautifulSoup(veekunaux, "lxml", from_encoding='utf8')
                    stats = veekun.find_all("div", class_="dex-pokemon-stats-bar")
                    ps = stats[0].text
                    ataque = stats[1].text
                    defensa = stats[2].text
                    ataqueEsp = stats[3].text
                    defensaEsp = stats[4].text
                    velocidad = stats[5].text

                    for type in tipospk:
                        types[type] = Tipo(tipo=type)

                    for ability in habilidades:
                        abilities[ability] = Habilidad(habilidad=ability)
                    for egggp in ghuevo:
                        egggroups[egggp] = GrupoHuevo(grupo_huevo=egggp)

                    Tipo.objects.bulk_create(types.values())
                    Habilidad.objects.bulk_create(abilities.values())
                    GrupoHuevo.objects.bulk_create(egggroups.values())

                    writer.add_document(nombre=nombre, numPokedex=str(numpokedex), generacion=generacion,
                                        habilidad=habilidades, habitat=habitat, color=color,
                                        grupohuevo=ghuevo, imagenurl=imagenurl, tipos= tipospk, ps= int(ps),ataque= int(ataque),
                                        defensa= int(defensa), ataqueEsp= int(ataqueEsp), defensaEsp= int(defensaEsp),
                                        velocidad= int(velocidad))
                    i += 1
                    pokemons[numpokedex] = Pokemon(nombre=nombre, num_pokedex=numpokedex,generacion=generacion,url_imagen=imagenurl,
                                                   habitat=habitat,color=color, ps= int(ps), ataque= int(ataque),defensa= int(defensa),
                                                   ataque_especial= int(ataqueEsp),defensa_especial= int(defensaEsp), velocidad= int(velocidad),
                                                   habilidades = abilities, tipos= types, grupos_huevo=egggp)

        writer.commit()
        Pokemon.objects.bulk_create(pokemons.values())

        print(str(len(pokemons)) + ' Pokemon insertados')
    return Pokemon.objects.count()

#Definimos esquema WOOSH para consultas más rápidas
def get_schema():
    return Schema(nombre=TEXT(stored=True), numPokedex=ID(stored=True), generacion=NUMERIC(stored=True), habilidad=TEXT,
                  habitat=TEXT, color=TEXT(stored=True),grupohuevo=TEXT(stored=True), imagenurl=TEXT(stored=True),
                  tipos=TEXT(stored=True),ps=NUMERIC(stored=True),ataque=NUMERIC(stored=True),defensa=NUMERIC(stored=True),
                  ataqueEsp=NUMERIC(stored=True), defensaEsp=NUMERIC(stored=True),velocidad=NUMERIC(stored=True))