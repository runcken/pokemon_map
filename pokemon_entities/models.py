from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='media',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    description = models.TextField(null=True)
    title_en = models.TextField(null=True)
    title_jp = models.TextField(null=True)
    previous_pokemon = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True
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
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
