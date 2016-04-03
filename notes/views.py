from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib import auth

from notes.models import Notes, Category

# Create your views here.
def hello(request):
    args = {}
    return render_to_response('notes.html', args)


def notes(request):
    args = {}

    args['username'] = auth.get_user(request).username
    print(args['username'])
    args['notes'] = Notes.objects.filter(author=auth.get_user(request).id)
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)

def note(request, id=None):
    args = {}
    args['note'] = Notes.objects.get(id=id, author=auth.get_user(request).id)
    args['username'] = auth.get_user(request).username
    args['projects'] = Category.objects.all()
    return render_to_response('note.html', args)



def category(request, category_id=1):
    args = {}
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.get(id=category_id)
    args['notes'] = Notes.objects.filter(category=category_id, author=auth.get_user(request).id)
    args['username'] = auth.get_user(request).username
    # branch_categories = args['category'].get_descendants(include_self=True)
    # args['category_articles'] = Notes.objects.filter(category__in=branch_categories).distinct()
    return render_to_response('category.html', args)