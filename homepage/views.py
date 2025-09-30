# PowerShell-friendly: just save as homepage/views.py
from django.shortcuts import render

# Homepage view
def index(request):
    return render(request, "homepage/index.html")
