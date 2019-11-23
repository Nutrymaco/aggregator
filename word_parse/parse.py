import pymorphy2
import redis
import re


# TODO: add function, which search close words
def lemmatization(text):
    key_words = []
    morph = pymorphy2.MorphAnalyzer()
    for word in text.split(' '):
        key_words.append(morph.parse(word)[0].normal_form)
    return key_words


def delete_tags(text) -> str:
    replace_list = re.findall('</?[a-z]{1,8}[1-6]?>?', text)
    for repl in replace_list:
        text = text.replace(repl, '')

    return text



