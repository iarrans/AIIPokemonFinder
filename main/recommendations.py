#encoding:utf-8

from math import sqrt

# Returns a distance-based similarity score for person1 and person2
from main.models import Pokemon


def sim_distance(person1, person2):
    ps = pow(person1.ps - person2.ps, 2)
    ataque =  pow(person1.ataque - person2.ataque, 2)
    defensa = pow(person1.defensa - person2.defensa, 2)
    ataqueesp = pow(person1.ataque_especial - person2.ataque_especial, 2)
    defensaesp = pow(person1.defensa_especial - person2.defensa_especial, 2)
    velocidad = pow(person1.velocidad - person2.velocidad, 2)

    distancia = sqrt(ps + ataque + defensa + defensaesp + ataqueesp + velocidad)
    return distancia

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(inicial, n=3, similarity=sim_distance):
    pokemons = Pokemon.objects.all()
    scores = [(similarity(inicial, other), other)
                for other in pokemons if other != inicial]
    scores.sort(key = lambda x: x[0])
    print(scores)
    return scores[0:n]

