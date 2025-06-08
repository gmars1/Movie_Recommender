from django.shortcuts import render
from .models import Movie, UserMovieRating
from django.contrib.auth import login
from .forms import SignUpForm, RateMovieForm
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg, F, Count
from django.db.models.functions import Round


def movie_list(request):
    # Аннотируем и сортируем: сначала по убыванию средней оценки (NULLS LAST), потом по названию
    movie_list_qs = Movie.objects.annotate(
        avg_rating_calc=Round(Avg('usermovierating__rating'), 1)
    ).order_by(F('avg_rating_calc').desc(nulls_last=True), 'title_ru')
    paginator = Paginator(movie_list_qs, 10) # Показывать по 10 фильмов на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'films/movie_list.html', {'page_obj': page_obj})

def signup(request):
   if request.method == 'POST':
       form = SignUpForm(request.POST)
       if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('movie_list')
   else:
       form = SignUpForm()
   return render(request, 'registration/signup.html', {'form': form})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie.objects.prefetch_related('genres', 'actors'), id=movie_id)
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating_obj = UserMovieRating.objects.get(user=request.user, movie=movie)
            user_rating = user_rating_obj.rating
        except UserMovieRating.DoesNotExist:
            pass # У пользователя еще нет оценки для этого фильма

    if request.method == 'POST' and request.user.is_authenticated:
        form = RateMovieForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            # Обновляем или создаем оценку
            UserMovieRating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'rating': rating_value}
            )
            return redirect('movie_detail', movie_id=movie.id) # Перезагружаем страницу, чтобы показать обновленную оценку
    else:
        initial_data = {'rating': user_rating} if user_rating else {}
        form = RateMovieForm(initial=initial_data)

    # Получение похожих фильмов
    similar_movies = []
    if movie.genres.exists(): # Проверяем, есть ли у фильма жанры
        movie_genre_ids = movie.genres.values_list('id', flat=True)
        similar_movies = Movie.objects.filter(genres__id__in=movie_genre_ids) \
                                      .exclude(id=movie.id) \
                                      .annotate(common_genres_count=Count('genres')) \
                                      .order_by('-common_genres_count', '-rating__rating')[:5] # Показываем до 5 похожих фильмов
    
    context = {
        'movie': movie, 
        'rate_form': form, 
        'user_rating': user_rating,
        'similar_movies': similar_movies # Добавляем похожие фильмы в контекст
    }
    return render(request, 'films/movie_detail.html', context)
