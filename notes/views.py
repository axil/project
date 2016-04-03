from django.core.checks import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, \
    redirect
from django.contrib import auth
from django.template.context_processors import csrf

from notes.models import Notes, Category
from notes.forms import NoteForm

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

def note_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    args = {}
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    form = NoteForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')
    context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
    context['projects'] = Category.objects.all()
    return render(request, "note_edit.html", context)
    # return HttpResponse(id[:-1])



def note_del(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    instance.delete()
    return redirect('/')