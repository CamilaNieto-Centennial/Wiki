from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django.http import HttpResponseRedirect

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
