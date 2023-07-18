from django.shortcuts import render, redirect
from base import forms
from base import models

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.exceptions import EmptyResultSet

from django.core.mail import EmailMessage, get_connection
from trivia import settings

from email.mime.text import MIMEText
import ssl
import smtplib
import uuid

from datetime import datetime
import ast
import json

# from base.services import fetch_data
from base.services.fetch_data import FetchTriviaData
from base.services.utils import get_results, get_total_points, get_total_time, score_redirect
from base import trivia
from base.templatetags.triviatags import translate 

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
                messages.error(request, 'Email or password incorrect')
    
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
    if not request.user.is_authenticated:
        return redirect('login')
    
    if score_redirect(request):
        return redirect('home')
    
    if request.method == "POST":
        question = request.session.get('questions')
        user = request.user
        
        result = trivia.is_correct(question, request.POST)
        user.add_answered()
        if result:
            user.add_points(int(request.POST.get('bet')))
            user.add_correctly()
        else:   
            user.subtract_points(int(request.POST.get('bet')))

    question = {}

    while not question.get('question'):
        try:
            question = trivia.get_question('https://opentdb.com/api.php', request.user) 
        except (request.HTTPError, request.ConnectionError):
            continue
        
    if not question:
        raise EmptyResultSet("No question found, please try again later")
    
    request.session['questions'] = question
    bet = trivia.get_bet_percentage(request.user.points)
        
    context = {
        "question": question,
        "bet": bet,
    }
    return render(request, 'game.html', context)      
   
   
def questions_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    result = ''
    
    if request.method == 'POST':
        answer = request.POST.get("answer")
        correct = request.session.get('questions')
        print(correct['answers'])
        print(f"answer: {answer} | correct: {correct['correct_answer']}")
        if answer == correct["correct_answer"]:
            result = 'correct'
        else:
            result = 'incorrect'
    
    # return HttpResponse(json.dumps({'result': result, "correct_a": correct["correct_answer"]}), content_type="application/json", status=200)
    return JsonResponse({'result': result, "correct_a": correct["correct_answer"], "correct_a_trans": translate(correct["correct_answer"])})


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

def get_points_request(request):
    if request.method == 'POST':
        user = models.CustomUser.objects.filter(id=request.user.id).first()
        token = str(uuid.uuid4())
        requested = datetime.now()
        user.request_points_key = token
        user.request_points_requested = str(requested)
        user.save()
        url = request.get_host()
        # TODO: armar una clase
        content=f"""
        Hola aca te mando un link para conseguir mas puntos!
        {url}/redeem_points/?key={user.request_points_key}
        """

        subject= "Hola aca tenemos mas puntos para vos!"
        
        # typical values for text_subtype are plain, html, xml
        text_subtype = 'plain'
        msg = MIMEText(content, text_subtype)
        msg['Subject'] =       subject
        msg['From'] = settings.EMAIL_HOST_USER
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as smtp:
                smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                smtp.sendmail(
                    settings.EMAIL_HOST_USER,
                    ["juanpablochoter@gmail.com"], 
                    msg.as_string()
                )
            messages.success(request, "Te enviamos un email con un link para recibir los puntos!")
        except Exception as e:
            print(e)
            messages.error(request, "Error al enviar el email")
        
        
    return redirect('home')    


def redeem_points(request):
    if request.GET.get('key'):
        user = models.CustomUser.objects.filter(request_points_key=request.GET.get('key'))
        if user:
            user.update(points=500, request_points_key='', request_points_requested='')

    context = {
    }
    return render(request, 'redeem_points.html', context)


def chat_room(request):
    context = {
        
    }
    
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    context = {
        "room": room_name
    }
    
    return render(request, 'chat/room.html', context)

# TODO: pantalla inicial
# TODO: sistema de email para enviar un email para pedir recarga de puntos falta armar email
# TODO: ranking sumar info
# TODO: crear sistema para ver si un user esta online
# TODO: implementar desafio, django channels juego online
# TODO: mensajeria, notificaciones
# TODO: crear base de datos para guardar amigos
# TODO: crear chat online con otros users
# TODO: eliminar historial para que no se pueda volver atras (solo dejar home, ver si puedo identificar que pagina es)


# Borderlands (PS3) | usd 2
# Borderlands 2 (PS3) | usd 5
# The Last of Us (PS3) | usd 10
# The Elder Scrolls IV: Oblivion (PS3) | usd 10
# The Elder Scrolls IV: Shivering Isles (PS3) | usd 10 
# Bioshock Infinite (PS3) | usd 5
# Dragon Age Origins: Ultimate Edition (PS3) | usd 10
# Dragon Age: Origins Awakening (PS3) | usd 10
# Dragon Age 2 (PS3) | usd 10
# Battlefield 3 (PS3) | usd 5
# God of War: Saga Collection (PS3) | usd 25
# Mass Effect Trilogy (PS3) | usd 10
# Kingdom Hearts HD 1.5 Remix (PS3) | usd 10
# Dead Space (PS3) | usd 10
# Dark Souls (PS3) | usd 10


# The Elder Scrolls V: Skyrim Special Edition (PS4) | usd 8
# The Elder Scrolls V: Skyrim (PS4) | usd 5
# The Elder Scrolls Online: Imperial Edition (PS4) | usd
# The Witcher 3: Wild Hunt (PS4) | usd 8
# Destiny - Standard Edition (PS4) | usd 5
# Prey (PS4) | usd 5
# Dark Souls III: The Fire Fades (PS4) | usd 5
# Bloodborne (PS4) | usd 8
# Battlefield V (PS4) | usd 8
# Far Cry 5 (PS4) | usd 6
# Star Wars: Battlefront (PS4) | usd 5
# Merge Games Yonder The Cloud Catcher Chronicles (PS4) | usd 8
# Dragon Age Inquisition (PS4) | usd 8
# Spyro Trilogy Reignited (PS4) | usd 10
# Doom: Eternal (PS4) | usd 8
# God of War Hits (PS4) | usd 8
# Fallout 4 - (PS4) | usd 8
# Mass Effect Andromeda - (PS4) | usd 8