from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.home, login_url='login'), name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("game/", login_required(views.game_view, login_url='login'), name="game_view"),
    path('questions_form/', login_required(views.questions_form, login_url='login'), name='questions_form'),
    path('ranking/', login_required(views.players_rankings, login_url='login'), name='players_rankings'),
    path('wrong/', login_required(views.wrong_answer, login_url='login'), name='wrong_answer'),
    path('get_points_request/', login_required(views.get_points_request, login_url='login'), name='get_points_request'),
    path('redeem_points/', views.redeem_points, name='redeem_points'),
    
    path('chat-room/', views.chat_room, name='chat_room'),
    path('chat-room/<str:room_name>', views.room, name='room'),
]