from GameStreams.models import Stream
from django import forms


# Create the form class.
class UrlForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['url']


class WordForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea, label='Ключевые слова', )
