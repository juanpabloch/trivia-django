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
import logging

from datetime import datetime
import ast
import json

# from base.services import fetch_data
from base.services.fetch_data import FetchTriviaData
from base.services.utils import get_results, get_total_points, get_total_time, score_redirect
from base import trivia
from base.templatetags.triviatags import translate 

UserModel = get_user_model()
logger = logging.getLogger(__name__)

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
            points = trivia.get_points(int(request.POST.get('bet')), int(request.POST.get("current_time")))
            user.add_points(points)
            user.add_correctly()
        else:   
            user.subtract_points(int(request.POST.get('bet')))

    question = {}

    while not question.get('question'):
        try:
            question = trivia.get_question('https://opentdb.com/api.php', request.user) 
        except (request.HTTPError, request.ConnectionError):
            logger.error('No connection to the API', exc_info=True)
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
        correct = request.session.get('questions')
        answer = request.POST.get("answer")
        bet = request.POST.get('bet')
        time = int(request.POST.get('time'))
        
        if answer == correct["correct_answer"]:
            result = 'correct'
            points = trivia.get_points(int(bet), time)
        else:
            result = 'incorrect'
            points = int(bet)
    
    return JsonResponse({
        "result": result, 
        "points": points,
        "correct_a": correct["correct_answer"], 
        "correct_a_trans": translate(correct["correct_answer"])
    })


def players_rankings(request):
    try:
        ranking = models.CustomUser.objects.all().order_by('-points')
    except Exception as e:
        logger.error(f'Error getting players ranking: {e}', exc_info=True)
    
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
        except Exception as e:
            logger.error(f'Error returning a wrong answer: {e}', exc_info=True)
            return HttpResponse(status=500)
    
    return redirect('home')    


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
        
        text_subtype = 'plain'
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
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
            logger.error(f'Error sending points request email: {e}', exc_info=True)
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
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            return redirect('room', room_name=name)
        
    context = {}
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    context = {
        "room": room_name
    }
    
    return render(request, 'chat/room.html', context)


# TODO: deploy python anyware revisar archivos 
# TODO: refactorizar codigo + OPP
# TODO: pantalla inicial
# TODO: sistema de email para pedir recarga de puntos falta armar email
# TODO: premios a la racha 5 seguidas 10 seguidas 20 seguidas 30 seguidas
# TODO: implementar desafio, django channels juego online
# TODO: crear base de datos para guardar amigos
# TODO: crear sistema para ver si un user esta online
# TODO: mensajeria, notificaciones
# TODO: crear chat online con otros users
# TODO: puntajes por semana y un premio al mejor de la semana