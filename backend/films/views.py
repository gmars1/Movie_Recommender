from django.shortcuts import render
from .models import Movie
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def movie_list(request):
    movie_list_all = Movie.objects.all().order_by('title_ru') # Сортируем для консистентности
    paginator = Paginator(movie_list_all, 10) # Показывать по 10 фильмов на странице

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
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'films/movie_detail.html', {'movie': movie})