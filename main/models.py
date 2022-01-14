
from django.db import models
import django.db.models.fields

class Tipo(models.Model):
    tipo = models.TextField()

    def __str__(self):
        return self.tipo

class GrupoHuevo(models.Model):
    grupo_huevo = models.TextField(verbose_name='Grupo Huevo')

    def __str__(self):
        return self.grupo_huevo

class Habilidad(models.Model):
    habilidad = models.TextField(verbose_name='Habilidad')

    def __str__(self):
        return self.habilidad

class Pokemon(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    num_pokedex = models.IntegerField(verbose_name='numPokedex')
    generacion = models.IntegerField(verbose_name='Generacion')
    habilidades = models.ManyToManyField(Habilidad)
    habitat = models.TextField(verbose_name='Habitat')
    color = models.TextField(verbose_name='Color')
    url_imagen = models.TextField(verbose_name='Url imagen')
    grupos_huevo = models.ManyToManyField(GrupoHuevo)
    tipos = models.ManyToManyField(Tipo)
    ps = models.IntegerField(verbose_name='PS')
    ataque = models.IntegerField(verbose_name='Ataque')
    defensa = models.IntegerField(verbose_name='Defensa')
    ataque_especial = models.IntegerField(verbose_name='Ataque Especial')
    defensa_especial = models.IntegerField(verbose_name='Defensa Especial')
    velocidad = models.IntegerField(verbose_name='Velocidad')

    def __str__(self):
        return self.nombre

