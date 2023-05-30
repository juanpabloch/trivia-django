from django import template
from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='auto', target='es')
register = template.Library()


@register.filter
def translate(string):
    trans_string = ''
    try:
        trans_string = translated.translate(string)
    except:
        trans_string = string
        
    return trans_string


@register.filter
def translate_(question):
    print("QUESTION: ", question)
    trans_question = {}
    trans_question['question'] = translated.translate(question['question'])
    
    try:
        trans_question['answers'] = [translated.translate(answer) for answer in question['answers']]
        trans_question['correct'] = translated.translate(question['correct_answer'])
    except:
        trans_question['answers'] = [answer for answer in question['answers']]
        trans_question['correct'] = question['correct_answer']
        
    trans_question['category'] = translated.translate(question['category'])
    return trans_question


register.filter("translate", translate)
register.filter("translate_", translate_)