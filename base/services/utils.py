from base import models
from datetime import datetime

def get_categories():
    cate = models.Category.objects.all().values()
    categories = tuple( (item["number"], item["name"]) for item in cate )
    return categories


def get_difficulty():
    difficulty = (
        ("easy", "Facil"),
        ("medium", "Normal"),
        ("hard", "Dificil")
    )
    return difficulty


def get_results(questions, answers):  
    points = 0

    for i, question in enumerate(questions):
        if question["correct_answer"] == answers[f"question_{i+1}"]:
            points += 1

    return points


def get_total_points(points, difficulty):
    total_points = points
    if difficulty == "medium":
        total_points = points*1.5
    elif difficulty == "hard":
        total_points = points*2
        
    return total_points


def get_total_time(start, end):
    start_time = datetime.strftime(start, '%Y-%m-%d %H:%M:%S.%f')
    end_time = datetime.strftime(end, '%Y-%m-%d %H:%M:%S.%f')
    difference = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    seconds_in_day = 24 * 60 * 60

    result = divmod(difference.days * seconds_in_day + difference.seconds, 60)
    
    return result