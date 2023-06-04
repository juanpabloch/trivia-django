from django.shortcuts import render, redirect
from base import forms
from base import models

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

from datetime import datetime
import ast
import json

# from base.services import fetch_data
from base.services.fetch_data import FetchTriviaData
from base.services.utils import get_results, get_total_points, get_total_time, score_redirect
from base import trivia
from base.templatetags import triviatags

UserModel = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {
                    "error": "invalid user",
                    "form": forms.LoginForm()
                }
                return render(request, 'registration/login.html', context)
    form = forms.LoginForm()
    context = {
        "form": form
    }
    return render(request, 'registration/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
            
    form = forms.RegisterForm()
    context = {
        "form": form
    }
    
    return render(request, 'registration/register.html', context)


def logout(request):
    logout(request)
    return redirect('login')


def home(request):
    top_ten = models.CustomUser.objects.all().order_by('-points')[:10]
    context = {
        "player" : request.user,
        "top_ten" : top_ten
    }
    return render(request, 'index.html', context)


def game_view(request):
    if score_redirect(request):
        return redirect('home')
    
    flag = True
    bet = {}

    while flag:
        question = trivia.get_question('https://opentdb.com/api.php')
        if question.get('question'):
            request.session['questions'] = question
            bet = trivia.get_bet_percentage(request.user.points)
            flag = False            
    
    context = {
        "question": question,
        "bet": bet,
    }
    return render(request, 'game.html', context)      
   
   
def questions_form(request):
    if request.method == "POST":
        print("POST QUESTION")
        question = request.session.get('questions')
        user = request.user
        print("CORRECTION")
        result = trivia.is_correct(question, request.POST)
        user.add_answered()
        if result:
            user.add_points(int(request.POST.get('bet')))
            user.add_correctly()
        else:   
            user.subtract_points(int(request.POST.get('bet')))

        context = {
            "result": result
        }
        return render(request, 'result.html', context)
    
    return redirect('home')


def players_rankings(request):
    try:
        ranking = models.CustomUser.objects.all().order_by('-points')
    except Exception as err:
        print(err)
    
    context = {
        "ranking" : ranking
    }

    return render(request, 'ranking.html', context)


def wrong_answer(request):
    if request.method == 'POST':
        try:
            request.user.add_answered()
            request.user.subtract_points(int(request.POST.get('bet')))
            return HttpResponse(status=200)
        except Exception as err:
            print(err)
            return HttpResponse(status=500)
    
    return redirect('home')    
        
"""
    USER:  [
        'active', 'add_answered', 'add_correctly', 'add_points', 'banned', 'check', 'check_password', 'clean', 
        'clean_fields', 'country', 'date_error_message', 'date_joined', 'delete', 'email', 
        'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 
        'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 
        'get_next_by_register', 'get_next_by_update', 'get_previous_by_date_joined', 'get_previous_by_register', 
        'get_previous_by_update', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 
        'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 
        'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 
        'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 
        'pk', 'points', 'prepare_database_save', 'q_answered', 'q_correctly', 'q_history', 'refresh_from_db', 'register', 
        'save', 'save_base', 'serializable_value', 'set_bet', 'set_password', 
        'set_unusable_password', 'subtract_points', 'unique_error_message', 'update', 'user_permissions', 
        'username', 'username_validator', 'validate_unique'
    ]
"""