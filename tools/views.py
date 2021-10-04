from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Notes, Todo

from .forms import GoogleSearchForm, WikipediaSearchForm, DictionarySearchForm, TranslatorForm, TodoForm, NotesForm

import requests
from googlesearch import search
from googletrans import Translator
import wikipediaapi
from PyDictionary import PyDictionary
wiki = wikipediaapi.Wikipedia('en')
dictionary = PyDictionary()
trans = Translator()


def index(request):
    quote = requests.get('https://zenquotes.io/api/random').json()
    context = {
        'quote': quote[0]["q"],
        'author': quote[0]["a"],
    }
    return render(request, 'tools/index.html', context=context)


@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            newTask = Todo(task=task, user=request.user)
            newTask.save()
            messages.success(request, 'New todo created successfully.')
            return redirect('todo')
        else:
            messages.error(request, 'Something went wrong!! Please try again')
    else:
        form = TodoForm()

    uncompletedTasks = request.user.todo_set.filter(completed=False).all()
    completedTasks = request.user.todo_set.filter(completed=True).all()

    context = {
        'title': "Todo",
        'form': form,
        'uncompletedTasks': uncompletedTasks,
        'completedTasks': completedTasks,
    }
    return render(request, 'tools/todo.html', context=context)


@login_required
def deleteTodo(request, id):
    if request.user.todo_set.filter(id=id).count():
        task = request.user.todo_set.filter(id=id)
        task.delete()
        messages.success(request, 'Todo deleted successfully.')
    else:
        messages.error(request, 'Something went wrong!! Please try again')

    return redirect('todo')


@login_required
def completeTodo(request, id):
    if request.user.todo_set.filter(id=id).count():
        task = request.user.todo_set.filter(id=id).first()
        task.completed = True
        task.save()
        messages.success(request, 'Todo marked as completed successfully.')
    else:
        messages.error(request, 'Something went wrong!! Please try again')

    return redirect('todo')


@login_required
def uncompleteTodo(request, id):
    if request.user.todo_set.filter(id=id).count():
        task = request.user.todo_set.filter(id=id).first()
        task.completed = False
        task.save()
        messages.success(request, 'Todo marked as uncompleted successfully.')
    else:
        messages.error(request, 'Something went wrong!! Please try again')

    return redirect('todo')


@login_required
def notes(request):
    notes = request.user.notes_set.all()
    context = {
        'title': "Notes",
        'notes': notes,
    }
    return render(request, 'tools/notes.html', context=context)


@login_required
def openNotes(request, id):
    if not request.user.notes_set.filter(id=id).count():
        return redirect('notes')
    else:
        note = request.user.notes_set.filter(id=id).first()
    context = {
        'title': "Notes",
        'note': note,
    }
    return render(request, 'tools/notesOpen.html', context=context)


@login_required
def createNotes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            newNote = Notes(title=title, content=content, user=request.user)
            newNote.save()
            messages.success(request, 'Notes created successfully.')
            return redirect('notes')
        else:
            messages.error(
                request, 'Something went wrong!! Please try again')
    else:
        form = NotesForm()
    context = {
        'title': "Notes",
        'form': form,
    }
    return render(request, 'tools/notesCreate.html', context=context)


@login_required
def editNotes(request, id):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = request.user.notes_set.filter(id=id).first()
            note.title = form.cleaned_data['title']
            note.content = form.cleaned_data['content']
            note.save()
            messages.success(request, 'Notes updated successfully.')
            return redirect('notes')
        else:
            messages.error(
                request, 'Something went wrong!! Please try again')
    else:
        note = request.user.notes_set.filter(id=id).first()
        formData = {
            'title': note.title,
            'content': note.content,
        }
        form = NotesForm(initial=formData)
    context = {
        'title': "Notes",
        'form': form,
    }
    return render(request, 'tools/notesEdit.html', context=context)


@login_required
def deleteNotes(request, id):
    if request.user.notes_set.filter(id=id).count():
        note = request.user.notes_set.filter(id=id)
        note.delete()
        messages.success(request, 'Note deleted successfully.')
    else:
        messages.error(request, 'Something went wrong!! Please try again')

    return redirect('notes')


def googleSearch(request):
    if request.method == 'POST':
        form = GoogleSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            searchResult = search(
                query, tld="co.in", num=10, stop=10, pause=2)
            context = {
                'title': "Search",
                'form': form,
                'query': query,
                'searchResult': searchResult,
            }
            return render(request, 'tools/googleSearch.html', context=context)
    else:
        form = GoogleSearchForm()

    context = {
        'title': "Search",
        'form': form,
    }
    return render(request, 'tools/googleSearch.html', context=context)


def wikipediaSearch(request):
    if request.method == 'POST':
        form = WikipediaSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            page = wiki.page(query)
            if page.exists():
                wikiPageTitle = page.title
                summary = page.summary
                wikiPageUrl = page.fullurl
                context = {
                    'title': "Wikipedia",
                    'form': form,
                    'wikiPageTitle': wikiPageTitle,
                    'summary': summary,
                    'wikiPageUrl': wikiPageUrl,
                }
                return render(request, 'tools/wikipediaSearch.html', context=context)
            else:
                messages.error(
                    request, f"Wikipedia Page not found for {query}")
    else:
        form = WikipediaSearchForm()

    context = {
        'title': "Wikipedia",
        'form': form,
    }
    return render(request, 'tools/wikipediaSearch.html', context=context)


def translator(request):
    if request.method == 'POST':
        form = TranslatorForm(request.POST)
        if form.is_valid():
            fromOption = form.cleaned_data['fromOption']
            toOption = form.cleaned_data['toOption']
            query = form.cleaned_data['query']
            result = trans.translate(query, src=fromOption, dest=toOption).text
            context = {
                'title': "Translator",
                'form': form,
                'fromOption': fromOption,
                'toOption': toOption,
                'result': result,
            }
            return render(request, 'tools/translator.html', context=context)
    else:
        form = TranslatorForm()
    context = {
        'title': "Translator",
        'form': form,
    }
    return render(request, 'tools/translator.html', context=context)


def dictionarySearch(request):
    if request.method == 'POST':
        form = DictionarySearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            option = form.cleaned_data['option']
            if option == 'meaning':
                searchResult = dictionary.meaning(query)
            elif option == 'synonym':
                searchResult = dictionary.synonym(query)
            else:
                searchResult = dictionary.antonym(query)

            context = {
                'title': "Dictionary",
                'form': form,
                'query': query,
                'option': option,
                'searchResult': searchResult,
            }
            return render(request, 'tools/dictionary.html', context=context)
    else:
        form = DictionarySearchForm()
    context = {
        'title': "Dictionary",
        'form': form,
    }
    return render(request, 'tools/dictionary.html', context=context)


def error_404(request,  exception):
    return render(request, 'tools/404.html')


def preloader(request):
    return render(request, 'tools/preloader.html')
