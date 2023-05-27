from django import template
from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='auto', target='es')
register = template.Library()


@register.filter
def translate(string):
    return translated.translate(string)


@register.filter
def translate_(question):
    trans_question = {}
    trans_question['question'] = translated.translate(question['question'])
    trans_question['answers'] = [translated.translate(answer) for answer in question['answers']]
    trans_question['category'] = translated.translate(question['category'])
    return trans_question


register.filter("translate", translate)
register.filter("translate_", translate_)