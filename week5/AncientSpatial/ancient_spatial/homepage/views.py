from django.shortcuts import render

# Create your views here.

def default(request):
    return render(request, "homepage/default.html")