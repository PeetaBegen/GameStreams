import json
from collections import Counter

from StreamParser.settings import MEDIA_ROOT, STATIC_ROOT
from pymorphy2 import MorphAnalyzer


def statistics(folder, filename):
    # words cloud
    with open('{}/words.txt'.format(STATIC_ROOT), 'r', encoding='utf-8') as f:
        words = [line.rstrip() for line in f]
    words_dict = {i: 0 for i in words}

    # json files to analyze
    with open('{}/{}/{}.json'.format(MEDIA_ROOT, folder, filename), 'r', encoding='utf-8') as f:
        data_json = json.load(f)  # type: dict

    morph = MorphAnalyzer()
    messages_words = []
    for text in data_json.values():
        for w in text.split(' '):
            messages_words.append(morph.parse(w)[0].normal_form)

    # statistics for all words
    messages_words_counts = Counter(messages_words)
    messages_words_counts['ВСЕГО СЛОВ'] = len(messages_words)
    with open('{}/{}/{}_COUNTER.json'.format(MEDIA_ROOT, folder, filename), 'w', encoding='utf-8') as f:
        json.dump(messages_words_counts, f, ensure_ascii=False)

    # statistics for word cloud
    for m in messages_words:
        if m in words_dict:
            words_dict[m] = words_dict[m] + 1

    with open('{}/{}/{}_WORD_CLOUD.json'.format(MEDIA_ROOT, folder, filename), 'w', encoding='utf-8') as f:
        json.dump(words_dict, f, ensure_ascii=False)
