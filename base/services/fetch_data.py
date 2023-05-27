import requests
import json
import random
from base import models

DIFFICULTY = ["easy", "medium", "hard"]

# def get_data(amount:int, category:int, difficulty:str):
#     response_api = requests.get(f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}")
#     data = json.loads(response_api.text)
#     return data


# def get_questions(data):
#     question_data = []

#     for i, question in enumerate(data["results"]):
#         new_result = {}
#         new_result["question_num"] = i+1
#         new_result["question"] = question['question']
#         new_result["correct_answer"] = question["correct_answer"]
#         new_result["answers"] = question["incorrect_answers"]
#         new_result["answers"].append(question["correct_answer"])
#         question_data.append(new_result)
    
#     return question_data


class FetchTriviaData():
    def __init__(self, url, amount:int=1):
        self.url = url + f'?amount={amount}'
        self.category = ''
    
    def get_data(self):
        categories = models.Category.objects.all()
        self.category = random.choice(categories)
        url = self.url + f'&category={self.category.number}' + f'&difficulty={random.choice(DIFFICULTY)}'
        print("URL: ", url)
        response_api = requests.get(url)
        data = json.loads(response_api.text)
        return data
    
            
    def get_questions(self):
        data = self.get_data()
        new_result = {}
        for i, question in enumerate(data["results"]):
            new_result["question_num"] = i+1
            new_result["question"] = question['question']
            new_result["correct_answer"] = question["correct_answer"]
            new_result["answers"] = question["incorrect_answers"]
            new_result["answers"].append(question["correct_answer"])
            new_result["category"] = self.category.name
            random.shuffle(new_result["answers"])

        return new_result
    
    
    def __str__(self) -> str:
        return self.url


class Game():
    def __init__(self, url, amount:int=1) -> None:
        self.url = url + f'?amount={amount}'
        self.category = ''
    
    def get_data(self):
        categories = models.Category.objects.all()
        self.category = random.choice(categories)
        url = self.url + f'&category={self.category.number}' + f'&difficulty={random.choice(DIFFICULTY)}'
        response_api = requests.get(url)
        data = json.loads(response_api.text)
        return data
    
    def get_question(self):
        data = self.get_data()
        new_result = {}
        for i, question in enumerate(data["results"]):
            new_result["question"] = question['question']
            new_result["correct_answer"] = question["correct_answer"]
            new_result["answers"] = question["incorrect_answers"]
            new_result["answers"].append(question["correct_answer"])
            random.shuffle(new_result["answers"])
            new_result["category"] = self.category.name

        return new_result