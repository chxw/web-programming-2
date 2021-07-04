from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


from . import util

from .forms import NewEntryForm, EditEntryForm

import markdown2
import random as rdm


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
    if request.method == 'POST':
        print(request.POST)
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            context = form.cleaned_data['context']
            # check if entry already exists
            if util.get_entry(title) != None:
                messages.error(request, 'Entry already exists')
                return redirect('new-entry')
            # else
            else:
                util.save_entry(title, context)
                return redirect(reverse('entry', kwargs={'title': title}))
    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/new_entry.html', {'form': form})

def edit_entry(request, title):
    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data['context']
            util.save_entry(title, context)
            return redirect(reverse('entry', kwargs={'title': title}))
    else:
        form = EditEntryForm(initial={'title': title, 'context': util.get_entry(title)})

    return render(request, 'encyclopedia/new_entry.html', {'form': form})

def random(request):
    entries = util.list_entries()
    return redirect(reverse('entry', kwargs={'title': rdm.choice(entries)}))