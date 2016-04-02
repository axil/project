from django.http import HttpResponse
from django.shortcuts import render, render_to_response


# Create your views here.
def hello(request):
    args = {}
    return render_to_response('notes.html', args)