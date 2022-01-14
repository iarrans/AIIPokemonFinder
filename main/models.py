
from django.db import models
import django.db.models.fields


class Pokemon(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    num_pokedex = models.IntegerField(verbose_name='numPokedex')
    generacion = models.IntegerField(verbose_name='Generacion')
    habilidades = models.TextField(verbose_name='Habilidades')
    habitat = models.TextField(verbose_name='Habitat')
    color = models.TextField(verbose_name='Color')
    url_imagen = models.TextField(verbose_name='Url imagen')
    grupos_huevo = models.TextField(verbose_name='GrupoHuevo')
    tipos = models.TextField(verbose_name='Tipos')
    ps = models.IntegerField(verbose_name='PS')
    ataque = models.IntegerField(verbose_name='Ataque')
    defensa = models.IntegerField(verbose_name='Defensa')
    ataque_especial = models.IntegerField(verbose_name='Ataque Especial')
    defensa_especial = models.IntegerField(verbose_name='Defensa Especial')
    velocidad = models.IntegerField(verbose_name='Velocidad')

    def __str__(self):
        return self.nombre

