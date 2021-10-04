from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todo/', views.todo, name='todo'),
    path('todo/delete/<int:id>/', views.deleteTodo, name='deleteTodo'),
    path('todo/complete/<int:id>/', views.completeTodo, name='completeTodo'),
    path('todo/uncomplete/<int:id>/', views.uncompleteTodo, name='uncompleteTodo'),
    path('notes/', views.notes, name='notes'),
    path('notes/create/', views.createNotes, name='createNotes'),
    path('notes/<int:id>/', views.openNotes, name='openNotes'),
    path('notes/delete/<int:id>/', views.deleteNotes, name='deleteNotes'),
    path('notes/edit/<int:id>/', views.editNotes, name='editNotes'),
    path('search/', views.googleSearch, name='googleSearch'),
    path('wikipedia/', views.wikipediaSearch, name='wikipediaSearch'),
    path('translator/', views.translator, name='translator'),
    path('dictionary/', views.dictionarySearch, name='dictionary'),
    path('preloader/', views.preloader, name='preloader'),
]
