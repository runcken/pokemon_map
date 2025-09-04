from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200,verbose_name='Имя')
    image = models.ImageField(
        upload_to='media',
        verbose_name='Изображение'
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    title_en = models.CharField(verbose_name='Имя(англ.)', blank=True)
    title_jp = models.CharField(verbose_name='Имя(япон.)', blank=True)
    previous_pokemon = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_pokemon',
        verbose_name='Предыдущий покемон'
        )  

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entities',
        verbose_name='Покемон'
        )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится')
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')