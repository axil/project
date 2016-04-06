import datetime
import json
from django.template import Context, RequestContext
from django.template.loader import  get_template

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf

from notes.models import Notes, Category
from notes.forms import NoteForm

# Create your views here.
def hello(request):
    args = {}
    return render_to_response('notes.html', args)


def notes(request, first='-date', second='title'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(publish=True).order_by(first, second)
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)


def categorysort(request, first='-date'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(
        author=auth.get_user(request).id).order_by('category', first)
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)

def sort_ajax(request, first='category'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(
        author=auth.get_user(request).id).order_by(first, '-date')
    args['projects'] = Category.objects.all()
    # import ipdb; ipdb.set_trace()

    t = get_template('notes_ajax.html')
    s = t.render(RequestContext(request,args))
    # import ipdb; ipdb.set_trace()

    return HttpResponse(s)

def favorites(request, first='-date'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(
        author=auth.get_user(request).id).order_by('-favorites', first)
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)

def filter_favorites(request, first='-date'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(favorites=True,
        author=auth.get_user(request).id).order_by(first)
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)

def filter_week(request):
    last_week = datetime.datetime.today() - datetime.timedelta(7)
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(
        date__range=(last_week, datetime.datetime.today()),
        author=auth.get_user(request).id).order_by('-date')
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)


def mynotes(request, first='-date', second='title'):
    args = {}
    args['username'] = auth.get_user(request).username
    args['notes'] = Notes.objects.filter(author=auth.get_user(request).id)\
        .order_by(first, second).select_related('category','author')
    args['projects'] = Category.objects.all()
    return render_to_response('notes.html', args)


def note(request, id=None):
    args = {}
    args['note'] = Notes.objects.get(id=id)
    args['username'] = auth.get_user(request).username
    args['projects'] = Category.objects.all()
    return render_to_response('note.html', args)


def category(request, category_id=1):
    args = {}
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.get(id=category_id)
    args['notes'] = Notes.objects.filter(category=category_id,
                                         author=auth.get_user(request).id)
    args['username'] = auth.get_user(request).username
    return render_to_response('category.html', args)

def note_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    args = {}
    args['username'] = auth.get_user(request).username
    args.update(csrf(request))
    args['projects'] = Category.objects.all()
    args['form'] = NoteForm()
    if request.POST:
        new_form = NoteForm(request.POST)
        if new_form.is_valid():
            instance = request.user
            instance = new_form.save(commit=False)
            instance.save()
            return redirect('/')
        else:
            args['form'] = new_form
    return render_to_response('create.html', args)

def note_edit(request, id=None):
    args = {}
    args['username'] = auth.get_user(request).username
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    form = NoteForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')
    args['title'] = instance.title
    args['instance'] = instance
    args['form'] = form
    args['projects'] = Category.objects.all()
    return render(request, "note_edit.html", args)


def note_del(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    instance.delete()
    return redirect('/')

def addfavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        note = Notes.objects.get(id=id)
        note.favorites = True
        note.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)


def removefavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        note = Notes.objects.get(id=id)
        note.favorites = False
        note.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)

