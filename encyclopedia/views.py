from django.shortcuts import render
from django.core.files.storage import default_storage
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
from markdown2 import Markdown

markdown = Markdown()

class NewEntryFormTitle(forms.Form):
    label = 'Title'
    title = forms.CharField(label=label)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, title):
    filenames = util.list_entries()
    # check if entry title is in filenames
    if title in filenames:
        # get content of file
        output = util.get_entry(title)
        # convert markdown to html
        content_converted = markdown.convert(output)
        # return entry page
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content_converted
        })
    # if title does not match any filenames
    return render(request, "encyclopedia/error.html", {
        "message": "Entry not found."
        })

def search(request):
    # get search query
    query = (request.GET.get('q')).capitalize()
    matches = []
    currentEntries = util.list_entries()
    # iterate through all entries to find the ones that match
    for currentEntry in currentEntries:
        # query matches name of the entry
        if currentEntry == query:
            output = util.get_entry(query)
            content_converted = markdown.convert(output)
            return render(request, "encyclopedia/entryPage.html", {
                "title": query,
                "content": content_converted
            })
            # query is a substring in the entry
        elif query in currentEntry:
            matches.append(currentEntry)
            return render(request, "encyclopedia/search.html", {
                "matches": matches
            })
    # query does not have any match
    return render(request, "encyclopedia/error.html", {
        "message": "No such entry."
    })

def newPage(request):
    if request.method == 'POST':
        # form for title of entry
        form1 = NewEntryFormTitle(request.POST)
        # text portion of the entry
        text = request.POST.get("markdown")
        if form1.is_valid():
            title = form1.cleaned_data["title"]
            currentEntries = util.list_entries()
            # title for new entry already exists
            if title in currentEntries:
                return render(request, "encyclopedia/error.html", {
                    "message": "An entry with this title already exists."
                })
            # save new entry
            util.save_entry(title, text)
            output = util.get_entry(title)
            content_converted = markdown.convert(output)
            return render(request, "encyclopedia/entryPage.html", {
                "title": title,
                "content": content_converted
            })

    return render(request, "encyclopedia/newPage.html", {
    "form1": NewEntryFormTitle(),
    })

def editPage(request, title):
    if request.method == 'GET':
        # return current content of entry in textarea
        text = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html", {
        "current_entry": text,
        "title": title
        })
    else:
        editedEntry = request.POST.get("editedEntry")
        # save edited entry
        util.save_entry(title, editedEntry)
        output = util.get_entry(title)
        content_converted = markdown.convert(output)
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content_converted
            })

def randomPage(request):
    currentEntries = util.list_entries()
    # choose a random entry
    randomEntry = random.choice(currentEntries)
    output = util.get_entry(randomEntry)
    content_converted = markdown.convert(output)
    return render(request, "encyclopedia/entryPage.html", {
    "title": randomEntry,
    "content": content_converted
    })
