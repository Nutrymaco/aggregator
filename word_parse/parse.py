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


# TODO: improve alghoritm with NLP
def get_id_list_from_text(text, prefix='word_') -> list:
    key_words = lemmatization(text)
    r = redis.Redis(host='redis', port=6379)
    id_list = list()

    for key_word in key_words:
        key_word_id_list = r.hkeys(prefix+key_word)

        for id in key_word_id_list:
            if id not in id_list:
                    id_list.append(id)

    return id_list