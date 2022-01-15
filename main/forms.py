# -*- encoding: utf-8 -*-
from django import forms

from main.models import Pokemon


class ColorForm(forms.Form):
    poke = Pokemon.objects.all()
    opciones_color = set()
    for pokemon in poke:
        if "/n" not in pokemon.color:
            opciones_color.add((pokemon.color,pokemon.color))
    colores = forms.select = forms.ChoiceField(widget=forms.Select, choices=opciones_color)

