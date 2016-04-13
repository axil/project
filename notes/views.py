import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from notes.models import Notes, Category
from notes.forms import NoteForm


def notes(request, first='-date_modified', second='title'):
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(publish=True).order_by(first, second)
            .select_related('category', 'author'),
        'category_all': Category.objects.all()
    }
    return render_to_response('notes.html', args)


@csrf_exempt
def my_notes(request):
    first = request.POST.get('first')
    second = request.POST.get('second')
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(
            author=auth.get_user(request)).order_by(first, second)
            .select_related('category', 'author'),
    }
    # tempate = get_template('notes_ajax.html')
    # import ipdb; ipdb.set_trace()
    return render_to_response('notes_ajax.html', args)


@csrf_exempt
def filter_date(request):
    date = int(request.POST.get('date'))
    last_date = datetime.datetime.today() - datetime.timedelta(date)
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(
            date_modified__gt=(last_date),
            author=auth.get_user(request)).order_by('date_modified')
        .select_related('category', 'author'),
    }
    return render_to_response('notes_ajax.html', args)


@csrf_exempt
def filter_favorites(request):
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(
            favorites=True,
            author=auth.get_user(request)).order_by('-date_modified')
        .select_related('category', 'author'),
    }
    return render_to_response('notes_ajax.html', args)


def note(request, id=None):
    args = {
        'note': Notes.objects.get(id=id),
        'username': auth.get_user(request).username,   # todo в шаблонах можно использовать request напрямую
        'category_all': Category.objects.all(),            # http://stackoverflow.com/questions/702592/django-request-in-template
    }
    return render_to_response('note.html', args)


def category(request, category_id=1):
    args = {
        'category_all': Category.objects.all(),
        'category': Category.objects.get(id=category_id),
        'notes': Notes.objects.filter(
            category=category_id,
            author=auth.get_user(request).id)
        .select_related('category', 'author'),
        'username': auth.get_user(request).username,
    }
    return render_to_response('category.html', args)


@login_required(login_url='/auth/login/')
def note_create(request):
    if not request.user:   # todo должно быть and
        raise Http404
    args = {
        'username':  auth.get_user(request).username,
        'category_all': Category.objects.all(),
        'form': NoteForm(),
    }
    args.update(csrf(request))
    if request.POST:
        new_form = NoteForm(request.POST)
        if new_form.is_valid():
            note = new_form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('/')
        else:
            args['form'] = new_form
    return render_to_response('create.html', args)


@login_required(login_url='/auth/login/')
def note_edit(request, id=None):
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    form = NoteForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/')
    args = {
        'username': auth.get_user(request).username,
        'title': instance.title,
        'instance': instance,
        'form': form,
        'category_all': Category.objects.all(),
    }
    return render(request, "note_edit.html", args)


@login_required(login_url='/auth/login/')
def note_del(request, id=None):
    args = {
        object: Notes.objects.filter(id=id,
                                     author=auth.get_user(request).id).delete()}
    args.update(csrf(request))
    return render_to_response('deleted.html', args)


def addfavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        Notes.objects.filter(id=id).update(favorites=True)
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)


def removefavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        Notes.objects.filter(id=id).update(favorites=False)
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)
