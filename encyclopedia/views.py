from django.shortcuts import render
from django.http import HttpResponse
#import markdown2
#from markdown2 import Markdown
import markdown

from . import util

#markdowner = Markdown()

# Index Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
def entry(request, name):
    if util.get_entry(name) == None:
        return HttpResponse("This page does not exist yet!")
    else:
        markdown.markdownFromFile(
        input = "entries/" + name + ".md",
        output = "encyclopedia/templates/entries/" + name + ".html",
        encoding= "utf8"
        )
        return render(request, "entries/" + name + ".html", {
            "name": util.get_entry(name)
        })
