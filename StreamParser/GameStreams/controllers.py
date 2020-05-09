import os

from GameStreams.models import Stream
from StreamParser.settings import MEDIA_ROOT, STATIC_ROOT


def save_form(url, folder, duration, channel, name, platform='YouTube'):
    """
    Save form data to DB
    :return:
    """
    stream = Stream()
    stream.url = url
    stream.folder = folder
    stream.duration = duration
    stream.channel = channel
    stream.name = name
    stream.platform = platform
    stream.save()


def get_folder_path():
    """
    Get folder of last stream analysis
    :return: path, folder
    """
    max_id = Stream.objects.latest('pk').id
    last_stream = Stream.objects.filter(pk=max_id)[0]

    return os.path.join(MEDIA_ROOT + '/' + last_stream.folder)


def get_last_query():
    """
    Get last query of GameStream parsing
    :return: str, channel_name + name + url
    """
    max_id = Stream.objects.latest('pk').id
    last_stream = Stream.objects.filter(pk=max_id)[0]
    return '{} : {}'.format(last_stream.folder, last_stream.url)


def get_keywords():
    """
    Get list of keywords
    :return: list
    """
    with open('{}/words.txt'.format(STATIC_ROOT), 'r', encoding='utf-8') as f:
        return [line.rstrip() for line in f]


def update_keywords(wordlist):
    """
    Update list of keywords
    :return:
    """
    with open('{}/words.txt'.format(STATIC_ROOT), 'w', encoding='utf-8') as f:
        for word in wordlist.split(','):
            f.write(word + '\n')
