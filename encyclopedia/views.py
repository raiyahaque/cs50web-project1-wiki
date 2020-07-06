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
    entry_title = f"{title}.md"
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        #print(filename)
        if entry_title == filename:
            output = util.get_entry(title)
            content_converted = markdown.convert(output)
            return render(request, "encyclopedia/entrypage.html", {
            "title": title,
            "content": content_converted
            })
    return render(request, "encyclopedia/error.html", {
        "message": "Entry not found."
        })

def search(request):
    query = (request.GET.get('q')).capitalize()
    matches = []
    currentEntries = util.list_entries()
    #if query.is_valid():
        #q = query.cleaned_data["q"]
    for currentEntry in currentEntries:
        if currentEntry == query:
            output = util.get_entry(query)
            content_converted = markdown.convert(output)
            return render(request, "encyclopedia/entrypage.html", {
                "title": query,
                "content": content_converted
            })
        elif query in currentEntry:
            matches.append(currentEntry)
            return render(request, "encyclopedia/search.html", {
                "matches": matches
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "No such entry."
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newPage(request):
    if request.method == 'POST':
        form1 = NewEntryFormTitle(request.POST)
        #print(form1)
        text = request.POST.get("markdown")
        if form1.is_valid():
            title = form1.cleaned_data["title"]
            #text = form2.cleaned_data["text"]
            #print(text)
            #print(title)
            #print(text)
            currentEntries = util.list_entries()
            #print(currentEntries)
            for currentEntry in currentEntries:
                if currentEntry == title:
                    return render(request, "encyclopedia/error.html", {
                        "message": "An entry with this title already exists."
                    })
            util.save_entry(title, text)
            output = util.get_entry(title)
            content_converted = markdown.convert(output)
            return render(request, "encyclopedia/entrypage.html", {
                "title": title,
                "content": content_converted
            })

    return render(request, "encyclopedia/newPage.html", {
    "form1": NewEntryFormTitle(),
    })

def editPage(request, title):
    if request.method == 'GET':
        text = util.get_entry(title)
        #print(text)
        return render(request, "encyclopedia/editPage.html", {
        "current_entry": text,
        "title": title
        })
    else:
        editedEntry = request.POST.get("editedEntry")
        util.save_entry(title, editedEntry)
        output = util.get_entry(title)
        content_converted = markdown.convert(output)
        return render(request, "encyclopedia/entrypage.html", {
            "title": title,
            "content": content_converted
            })

def randomPage(request):
    currentEntries = util.list_entries()
    randomEntry = random.choice(currentEntries)
    output = util.get_entry(randomEntry)
    #print(output)
    content_converted = markdown.convert(output)
    return render(request, "encyclopedia/entrypage.html", {
    "title": randomEntry,
    "content": content_converted
    })
