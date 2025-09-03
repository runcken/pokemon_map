import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    time_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.select_related('pokemon').filter(
        appeared_at__lte=time_now, disappeared_at__gte=time_now
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        image_url = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    
    if requested_pokemon:
        pokemon = requested_pokemon
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = pokemon.entities.filter(id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        image_url = request.build_absolute_uri(entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
    }
    if pokemon.previous_pokemon:
        pokemon_data['previous_evolution'] = ({
            'title_ru': pokemon.previous_pokemon,
            'pokemon_id': pokemon.previous_pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.previous_pokemon.image.url)
            })
    

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
