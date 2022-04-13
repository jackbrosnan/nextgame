from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib import messages
from .forms import RegisterForm, LikedGamesForm
from .models import *
from django.contrib.auth import authenticate, login as auth_login

from backend.model.game_matrix import GameSimilarityInfo

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(response, user)
            messages.success(response, f'Your account has been created! You are now able to log in!')
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})

# View for user submitting liked games form
def liked_games(response):
    all_liked = GameList.objects.filter(user=response.user.id).values_list('liked_game', flat=True)
    game_dict = {}
    for val in all_liked:
        for item in Game.objects.filter(id=val).values_list('title', 'cover'):
            game_dict[val] = item
    try:
        if response.method == "POST":
            form = LikedGamesForm(response.POST)
            if form.is_valid():
                l = form.save(commit=False)
                # checks if the submitted games are in Database
                if Game.objects.filter(title__contains=l.liked_game):
                    id = Game.objects.filter(title=l.liked_game).values_list('id', flat=True)
                    l.liked_game = id
                    l.name = '{}_list'.format(response.user)
                    l.user = response.user
                    form.save()
                    messages.success(response, f'You game has been submitted!')
                else:
                    messages.error(response, mark_safe('{}<br>Is not a valid game... Try again'.format(l.liked_game)))
            return redirect('/liked_games')
        else:
            form = LikedGamesForm()
    except ValueError:
        messages.error(response, 'You must be logged in to submit games...')
    return render(response, "main/liked_games.html", {'form': form, 'all_liked': game_dict})

# View for deleting user liked game from db
def delete_liked_game(response, id):
    game = GameList.objects.filter(user=response.user.id, liked_game=id)
    game.delete()
    return redirect('/liked_games')

# displays the game from search when user clicks it
def view(response):
    try:
        title = response.GET.get('title')
        qs = Game.objects.filter(title=title)
        images = qs.values('images')[0]
        images = list(images.values())
        img_list = images[0].split(',')
    # must click on object
    except IndexError:
        messages.error(response, 'Please select title from dropdown')
        return redirect('/lookup/')

    return render(response, "main/view.html", {'qs': qs,
                                               'image1': img_list[0],
                                               'image2': img_list[1],
                                               'image3': img_list[2],
                                               'image4': img_list[3],
                                               'image5': img_list[4],
                                               })

# View for user recommendations
@login_required
def recommendations(response):
    # Creating the GameSimInfo object
    game_sim_info = GameSimilarityInfo()

    # users liked games inside dictionary
    all_liked = GameList.objects.filter(user=response.user.id).values_list('liked_game', flat=True)
    users_liked_games = list(set(all_liked))

    rec_dict = {}
    if not users_liked_games:
        messages.error(response, mark_safe('Add your liked games to get recommendations!'))
        pass
    else:
        recommended_games = game_sim_info.get_recommendations(users_liked_games)
        # recommended_games_obj = Recommendation(user=response.user, rec_game=recommended_games)
        # recommended_games_obj.save()

        # game details
        for id in recommended_games:
            game = Game.objects.filter(id=id).values_list('title', 'cover')
            for item in game:
                rec_dict[id] = item

    return render(response, 'main/recommendations.html', {'games': users_liked_games, 'recommended': rec_dict})

def home(response):
    return render(response, "main/index.html", )

@login_required
def profile(request):
    user = request.user.id
    liked_game_count = GameList.objects.filter(user=user).count()

    return render(request, 'registration/profile.html', {'count': liked_game_count})

def search(request):
    return render(request, "main/search.html")

def search_title(request):
    titles = list()
    if 'title' in request.GET:
        qs = Game.objects.filter(title__icontains=request.GET.get('title'))
        for game in qs:
            titles.append(game.title)
    return JsonResponse({'data': titles})

def search_genre(request, genre):
    qs = Game.objects.filter(genres__contains=genre)
    return render(request, 'main/search_genre.html', {'qs': qs, 'genre': genre})

@login_required()
def login(response):
    return render(response, "registration/login.html",)