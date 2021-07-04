from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from . import util

import markdown2
import random as rdm


class NewEntryForm(forms.Form):
    title = forms.CharField(label='title')
    article = forms.CharField(widget=forms.Textarea, label="article")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if not title:
        title = request.session['query']
    title = title.capitalize()
    # check if entry exists
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    # return error.html
    return HttpResponseNotFound(f'<h1>404</h1> <p>{title} not found</p>')


def search(request):
    if request.method == 'GET':
        # save query to session
        request.session['query'] = request.GET.get('q')
        query = request.session['query']

        # subsearch
        entries = util.list_entries()
        found_entries = []
        for entry in entries:
            if query.lower() == entry.lower():
                return redirect(reverse('entry', kwargs={'title': entry}))
            elif query.lower() in entry.lower():
                found_entries.append(entry)

        return render(request, "encyclopedia/search_results.html", {
            "entries": found_entries
        })


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")


def random(request):
    entries = util.list_entries()
    return redirect(reverse('entry', kwargs={'title': rdm.choice(entries)}))
