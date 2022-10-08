from django.shortcuts import render
from django.http import HttpResponse
import markdown2

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

