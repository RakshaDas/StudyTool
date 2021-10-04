from django import forms
from tinymce.widgets import TinyMCE

import googletrans


class GoogleSearchForm(forms.Form):
    query = forms.CharField(required=True)


class WikipediaSearchForm(forms.Form):
    query = forms.CharField(required=True)


class TranslatorForm(forms.Form):
    fromOption = forms.ChoiceField(
        choices=(
            (k, v) for k, v in googletrans.LANGUAGES.items()
        ),
        initial='en',
        required=True
    )
    toOption = forms.ChoiceField(
        choices=(
            (k, v) for k, v in googletrans.LANGUAGES.items()
        ),
        initial='hi',
        required=True
    )
    query = forms.CharField(widget=forms.Textarea, required=True)


dictionaryOptions = (
    ("meaning", "Meaning"),
    ("synonym", "Synonym"),
    ("antonym", "Antonym"),
)


class DictionarySearchForm(forms.Form):
    query = forms.CharField(required=True)
    option = forms.ChoiceField(choices=dictionaryOptions, required=True)


class TodoForm(forms.Form):
    task = forms.CharField(required=True)


class NotesForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=TinyMCE())
