from django.contrib import admin
from .models import Movie, MovieRating, Genre, Actor, MovieGenre, MovieActor

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'created_at', 'updated_at')
    search_fields = ('title_ru',)

@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating',)
    search_fields = ('movie__title_ru',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name', 'created_at', 'updated_at')
    search_fields = ('genre_name',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at', 'updated_at')
    search_fields = ('full_name',)

# Можно также зарегистрировать MovieGenre и MovieActor, если нужно прямое управление ими,
# но обычно это не требуется, если они используются только как 'through' модели для ManyToMany.
# admin.site.register(MovieGenre)
# admin.site.register(MovieActor)
