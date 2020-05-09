import os
from zipfile import ZipFile

from GameStreams.chat_fetcher import youtube_scraper
from GameStreams.controllers import get_folder_path, update_keywords, get_keywords, get_last_query
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import UrlForm, WordForm


def get_url(request):
    initial_dict = {
        'words': ','.join(get_keywords()),
    }
    form = UrlForm()
    wordForm = WordForm(initial=initial_dict)
    if request.method == 'POST' and 'parsing' in request.POST:
        form = UrlForm(request.POST)
        if form.is_valid():
            youtube_scraper(form.cleaned_data['url'])
            return HttpResponseRedirect('/')
    elif request.method == 'POST' and 'keywords' in request.POST:
        wordForm = WordForm(request.POST)
        if wordForm.is_valid():
            update_keywords(wordForm.cleaned_data['words'])
            return HttpResponseRedirect('/')

    return render(request, 'index.html', {'form': form, 'wordForm': wordForm, 'last_query': get_last_query()})


def download(request):
    if request.method == 'GET':
        zip_filename = get_folder_path()
        output_filename = os.path.basename(zip_filename)
        filenames = [os.path.join(zip_filename, f) for f in os.listdir(zip_filename)]

        response = HttpResponse(content_type='application/zip')
        zip_file = ZipFile(response, 'w')
        for filename in filenames:
            zip_file.write(filename, '{}/{}'.format(output_filename, os.path.basename(filename)))
        zip_file.close()
        response['Content-Disposition'] = 'attachment; filename={}.zip'.format(output_filename)
        return response
