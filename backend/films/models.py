import uuid
from django.db import models
from django.db.models import Avg # Импортируем Avg
from django.contrib.auth.models import User # Импортируем стандартную модель User



class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_ru = models.CharField("Русское название", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Разрешаем NULL
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Разрешаем NULL

    # Связи M2M с существующими промежуточными таблицами
    genres = models.ManyToManyField('Genre', through='MovieGenre')
    actors = models.ManyToManyField('Actor', through='MovieActor')

    class Meta:
        db_table = 'movie'  # Указываем существующую таблицу

    def __str__(self):
        return self.title_ru

    def average_user_rating(self):
        # Рассчитываем среднюю оценку на основе UserMovieRating
        # self.usermovierating_set - это обратная связь от UserMovieRating к Movie
        avg_rating = self.usermovierating_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating is not None else None



class MovieRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Разрешаем NULL
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Разрешаем NULL

    class Meta:
        db_table = 'movierating'


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Разрешаем NULL
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Разрешаем NULL

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.genre_name


class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Разрешаем NULL
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Разрешаем NULL

    class Meta:
        db_table = 'actor'

    def __str__(self):
        return self.full_name


# Промежуточные модели для M2M
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genres' # Существующая таблица
        unique_together = (('movie', 'genre'),) # Отражает уникальность пары


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_actors' # Существующая таблица
        unique_together = (('movie', 'actor'),) # Отражает уникальность пары

class UserMovieRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", help_text="Оценка от 1 до 10")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'user_movie_rating'
        unique_together = ('user', 'movie') # Пользователь может оценить фильм только один раз

    def __str__(self):
        return f"{self.user.username} - {self.movie.title_ru}: {self.rating}"
