import requests
import json
import random
import math
from base import models

DIFFICULTY = ["easy", "medium", "hard"]
DIFFICULTY_EASY = ["easy"]
DIFFICULTY_START = ["easy", "medium"]
DIFFICULTY_MEDIUM = ["medium"]
DIFFICULTY_MEDIUM_HARD = ["medium", "hard"]
DIFFICULTY_HARD = ["hard"]


def get_data(api, points):
        categories = models.Category.objects.all()
        category = random.choice(categories)
        url = api + f'?amount=1' + f'&category={category.number}' + f'&difficulty={random.choice(get_dificulty(points))}'
        response_api = requests.get(url)
        data = json.loads(response_api.text)
        return data
    
    
def get_question(api, user):
        data = get_data(api, user.points)
        new_result = {}
        for i, question in enumerate(data["results"]):
            new_result["question"] = question['question']
            new_result["correct_answer"] = question["correct_answer"]
            new_result["answers"] = question["incorrect_answers"]
            new_result["answers"].append(question["correct_answer"])
            random.shuffle(new_result["answers"])
            new_result["category"] = question["category"]
            new_result["difficulty"] = question["difficulty"]

        return new_result


def is_correct(question, post):
    correct_answer = question.get("correct_answer")
    answer = post.get('answer')
    if correct_answer == answer:
        return True
    else:
        return False
    

def get_bet_percentage(points):
    bet = {
        "10": int((points*10)/100),
        "30": int((points*30)/100),
        "50": int((points*50)/100),
    }
    return bet


def get_points(points, time):
    if time > 10:
        if time < 20:
            return math.ceil(points * 1.1)
        else:
            return math.ceil(points * 1.3)
    else:
        return points


def get_dificulty(points):
    if points <= 50:
        return DIFFICULTY_EASY
    elif points > 50 and points <= 500:    
        return DIFFICULTY_START
    elif points > 500 and points <= 1500:
        return DIFFICULTY_MEDIUM 
    elif points > 1500 and points <= 3000:
        return DIFFICULTY_MEDIUM_HARD
    elif points > 3000:
        return DIFFICULTY_HARD
    
    
def response_process():
    pass