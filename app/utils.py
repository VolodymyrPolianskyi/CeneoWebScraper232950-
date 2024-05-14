import os
from deep_translator import GoogleTranslator

def extract(ancestor, selector, attribute = None , return_list = False):
    if return_list:
        if attribute:
            return [p[attribute] for p in ancestor.select(selector)]
        return [p.get_text().strip() for p in ancestor.select(selector)]
    if selector:
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute]
            except TypeError:
                return  None
        try:
            return ancestor.select_one(selector).get_text().strip()
        except AttributeError:
            return None
    if attribute:
        return ancestor[attribute]
    return None

def rate(score):
    score = score.split("/")
    return float(score[0].replace(",","."))/float(score[1].replace(",","."))
def reccomend(reccomendation):
    return True if reccomendation == 'Polecam' else False if reccomendation == 'Nie polecam' else None

def translate(text, from_lang = 'pl' , to_lang = 'en' ):
    if text:
        if isinstance(text, list):
            return {
                from_lang: text,
                to_lang: [GoogleTranslator(source = from_lang, target=to_lang).translate(t) for t in text]
            }
        return {
                from_lang: text, 
                to_lang: GoogleTranslator(source = from_lang, target=to_lang).translate(text)
        }
    return None

selectors = {
"opinion_id" :  [None , 'data-entry-id'],
"author" :  ['span.user-post__author-name'],
"recomendation" :  [".user-post__author-recomendation > em"],
"score" :  ["span.user-post__score-count"],
"content" :  [".user-post__text"],
"pros" :  ["div.review-feature__title--positives ~ div.review-feature__item", None , True,],
"cons" :  ["div.review-feature__title--negatives ~ div.review-feature__item", None , True,],
"helpful" :  ['button.vote-yes > span'],
"unhelpful" : [ 'button.vote-no > span'],
"publish" :  ['span.user-post__published > time:nth-child(1)' , 'datetime'],
"purchase" :  ["span.user-post__published > time:nth-child(2)" , 'datetime']
}

transformations = {
    "recomendation" :  reccomend,
    "score" :  rate,
    "helpful" :  int,
    "unhelpful" : int,
    'content' : translate,
    'pros' : translate,
    'cons' : translate
}