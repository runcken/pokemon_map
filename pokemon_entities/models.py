from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200,verbose_name='Имя')
    image = models.ImageField(
        upload_to='media',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    description = models.TextField(null=True,verbose_name='Описание', blank=True)
    title_en = models.TextField(null=True, verbose_name='Имя(англ.)', blank=True)
    title_jp = models.TextField(null=True, verbose_name='Имя(япон.)', blank=True)
    previous_pokemon = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='next_pokemon',
        verbose_name='Предыдущий покемон'
        )  

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон'
        )
    lat = models.FloatField(verbose_name='Широта', null=True)
    lon = models.FloatField(verbose_name='Долгота', null=True)
    appeared_at = models.DateTimeField(verbose_name='Появится', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет', null=True)
    level = models.IntegerField(verbose_name='Уровень', blank=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True)
