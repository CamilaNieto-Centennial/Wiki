from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django.http import HttpResponseRedirect
import random

from . import util

# Index Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
def entry(request, name):
    nameEntry = util.get_entry(name) # Access the .md file

    # Check if that page exists. If not display Error
    if nameEntry == None:
        error = "This page does not exist yet!"
        return render(request, "encyclopedia/error.html", {
            "error": error
        })
    # If exists, render "title" and "main" to entry.html file 
    else:
        mainContent = markdown2.markdown(nameEntry) # Covert md to HTML
        return render(request, "encyclopedia/entry.html", {
            "title": name,
            "main": mainContent
        })

# Search Feature
def search(request):
    if request.method == "POST":
        q = request.POST['q']

        listEntries = util.list_entries()
        page = ""

        # If the query typed is equal to one element of 'listEntries', update 'page' variable to the value of 'q'
        for listEntry in listEntries:
            if q.lower() == listEntry.lower():
                page = q
        # Redirect directly to the Entry Page
        if page != "":
            return HttpResponseRedirect("/wiki/" + page)
    

        results = []

        # Generate list of results according to the query typed
        for listEntry in listEntries:
            if q.lower() in listEntry.lower():
                results.append(listEntry) # Add new item to 'results' list
            
        return render(request, "encyclopedia/searchResults.html", {
            "search": q,
            "results": results
        })

# Create New Page
def create(request):
    # For POST request:
    if request.method == "POST":
        # Get 'title' and 'main' from the create page
        form = request.POST
        title = form['title']
        main = form['main']

        # Get list of entries
        listEntries = util.list_entries()

        # Validate when users does not type the 'title' or 'main'
        if title == "" or main == "":
            error = "Please fill out the title and main fields."
            return render(request, "encyclopedia/error.html", {
            "error": error
        })

        # Check that the new 'title', is NOT the same as one of the items inside of the List of Entries.
        for listEntry in listEntries:
            if title.lower() == listEntry.lower():
                error = "This page already exists. Please change the title!"
                return render(request, "encyclopedia/error.html", {
                    "error": error
                })
            else:
                # If the new entry only exists once on the list, then create a new .md file, and redirect the user to /wiki/title.
                util.save_entry(title, main)
                return HttpResponseRedirect("/wiki/" + title)

    # For GET request:
    elif request.method == "GET":
        return render(request, "encyclopedia/create.html")

# Edit Page
def edit(request, name):
    # For POST request:
    if request.method == "POST":
        # Get 'title' and 'main' from the create page
        form = request.POST
        title = form['title']
        main = form['main']

        # Save new changes
        util.save_entry(title, main)

        # Redirect to that Entry Page
        return HttpResponseRedirect("/wiki/" + title)

    # For GET request:
    elif request.method == "GET":
        # Get the title and content of .md file to show them on edit.html
        entry = util.get_entry(name) # Access the .md file

        return render(request, "encyclopedia/edit.html", {
            "title": name,
            "main": entry
        })

# Random Page
def randomPage(request):
    # Get list of entries and number of last Index of the List
    listEntries = util.list_entries()
    lastIndex = len(listEntries) - 1

    # Get a random number between 0 until 'lastIndex'
    randomNumber = random.randint(0, lastIndex)

    # Get the entry page with index of 'randomNumber'
    entry = listEntries[randomNumber]

    # Return random page
    return HttpResponseRedirect("/wiki/" + entry)
