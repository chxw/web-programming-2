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
    '''
    Render index page (index.html) with
    a list of all existing entries (retrieved using util.list_entries()).
    '''
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def handler404(request):
    '''
    Render 404 error page.
    '''
    response = render(request, "encyclopedia/404.html")
    response.status_code = 404
    return response


def entry(request, title):
    '''
    Render an entry page (entry.html) with
    the requested title (variable passed through function) and
    context of an entry (retrieved using util.get_entry()).
    '''
    # check if entry exists
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    # else return error.html
    return redirect(reverse('404'))


def search(request):
    '''
    Perform search on user's query (GET value) using a for loop.

    If the query matches an entry title exactly, return that page.
    If the query does not have an exact match, but has substring matches,
    then return a results page (search_results.html) with all matches.
    If there are no matches, the results page will display "No results found".
    '''
    if request.method == 'GET':
        # get GET query value (?q=value)
        query = request.GET.get('q')

        # get existing entries
        entries = util.list_entries()
        # search
        found_entries = []
        for entry in entries:
            # if exact search, redirect to that entry page
            if query.lower() == entry.lower():
                return redirect(reverse('entry', kwargs={'title': entry}))
            # if not exact string but substring, consider "found"
            elif query.lower() in entry.lower():
                found_entries.append(entry)

        # render results of substring search
        return render(request, "encyclopedia/search_results.html", {
            "entries": found_entries
        })


def new_entry(request):
    '''
    Create new entry based on user's form values.

    Form title char length must be <= 100.
    If form title matches an existing entry,
    the new entry will not be saved and user will receive error message.
    If new entry is saved successfully, redirect user to that entry page.
    '''
    if request.method == 'POST':
        # create new instance of form with POST request info
        form = NewEntryForm(request.POST)
        # validate and get data
        if form.is_valid():
            title = form.cleaned_data['title']
            context = form.cleaned_data['context']
            # if entry already exists, send error alert
            if util.get_entry(title) is not None:
                messages.error(request, 'Entry already exists')
                return redirect('new-entry')
            # else save new entry and redirect to that page
            else:
                util.save_entry(title, context)
                return redirect(reverse('entry', kwargs={'title': title}))

    # initial state (GET) is blank form
    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/new_entry.html', {'form': form})


def edit_entry(request, title):
    '''
    Edit existing entry based on user's form values.

    Title is not editable.
    Form is pre-populated using existing entry page data.
    '''
    if request.method == 'POST':
        # create new instance of form with POST request info
        form = EditEntryForm(request.POST)
        # validate and save entry
        if form.is_valid():
            context = form.cleaned_data['context']
            util.save_entry(title, context)
            return redirect(reverse('entry', kwargs={'title': title}))

    # initial state (GET) is pre-populated form
    else:
        form = EditEntryForm(
            initial={'title': title, 'context': util.get_entry(title)})

    return render(request, 'encyclopedia/edit_entry.html', {'form': form})


def random(request):
    '''
    Redirect user to random existing entry page.

    Random entry is generated using random library.
    '''
    return redirect(reverse('entry', kwargs={
        'title': rdm.choice(util.list_entries())
    }))
