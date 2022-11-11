from django.db import models
from datetime import date
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    # Категории
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    # Актеры и режиссеры
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Genre(models.Model):
    # Жанры
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Serial(models.Model):
    # Сериалы
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='serials/')
    year = models.PositiveIntegerField('Дата выхода', default=2000)
    country = models.CharField('Страна', max_length=100)
    # director = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    seasons = models.PositiveSmallIntegerField('Сезонов')
    series = models.PositiveSmallIntegerField('Серий')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('serial_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'


class SerialShots(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='serial_shots/')
    serial = models.ForeignKey(Serial, verbose_name='Сериал', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, verbose_name='сериал')

    def __str__(self):
        return f'{self.star} - {self.serial}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Название', max_length=100)
    text = models.TextField('Сообщение', max_length=1000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, verbose_name='сериал')

    def __str__(self):
        return f'{self.name} - {self.serial}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
