import datetime
from django.template import Context, RequestContext
from django.template.loader import  get_template
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from notes.models import Notes, Category
from notes.forms import NoteForm


def notes(request, first='-date', second='title'):
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(publish=True).order_by(first, second).
            select_related('category','author'),
        'projects': Category.objects.all()
    }
    return render_to_response('notes.html', args)


@csrf_exempt
def my_notes(request):
    first = request.POST.get('first')
    second = request.POST.get('second')
            # message =  first + ' ' + second
    args = {
        'username' : auth.get_user(request).username,
        'projects': Category.objects.all(),
        'notes': Notes.objects.filter(
            author=auth.get_user(request).id).order_by(first, second).
            select_related('category','author'),
    }
    tempate = get_template('notes_ajax.html')
    # import ipdb; ipdb.set_trace()
    return HttpResponse(tempate.render(RequestContext(request,args)))
                                # todo что-то мне кажется, что render или render_to_response тоже можно (и нужно)
                                # HttpResponse обязателен для json.dumps, а мы решили через шаблон слать клиенту

@csrf_exempt
def filter_date(request):
    date = int(request.POST.get('date'))
    last_date = datetime.datetime.today() - datetime.timedelta(date)
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(
            date__gt=(last_date),
            author=auth.get_user(request).id).order_by('date').
            select_related('category','author'),
        'projects': Category.objects.all(),
    }
    tempate = get_template('notes_ajax.html')
    return HttpResponse(tempate.render(RequestContext(request,args)))

@csrf_exempt
def filter_favorites(request):
    args = {
        'username': auth.get_user(request).username,
        'notes': Notes.objects.filter(
            favorites=True,
            author=auth.get_user(request).id).order_by('-date').        # todo проверить как будет работать с
            select_related('category','author'),                        # неавторизованным юзером
        'projects': Category.objects.all(),
    }
    tempate = get_template('notes_ajax.html')
    return HttpResponse(tempate.render(RequestContext(request,args)))


def note(request, id=None):
    args = {
        'note': Notes.objects.get(id=id),
        'username': auth.get_user(request).username,   # todo в шаблонах можно использовать request напрямую
        'projects': Category.objects.all(),            # http://stackoverflow.com/questions/702592/django-request-in-template
    }
    return render_to_response('note.html', args)


def category(request, category_id=1):
    args = {
        'projects': Category.objects.all(),
        'category': Category.objects.get(id=category_id),
        'notes': Notes.objects.filter(category=category_id,
                                      author=auth.get_user(request).id),
        'username': auth.get_user(request).username,
    }
    return render_to_response('category.html', args)


def note_create(request):
    if not request.user.is_staff or not request.user.is_superuser:   # todo должно быть and
        raise Http404
    args = {
        'username':  auth.get_user(request).username,
        'projects': Category.objects.all(),
        'form': NoteForm(),
    }
    args.update(csrf(request))
    if request.POST:
        new_form = NoteForm(request.POST)
        if new_form.is_valid():
            instance = new_form.save(commit=False)     # todo commit=False обязателен если дальше будет save_m2m()
            instance.save()                            # если его нет, лучше в одну строчку с commit=True
            return redirect('/')
        else:
            # args.update(form(new_form))
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
        return redirect('/')       # todo лучше перенаправлять хотя бы на страницу заметки
    args = {
        'username': auth.get_user(request).username,
        'title': instance.title,
        'instance': instance,
        'form': form,
        'projects': Category.objects.all(),    # todo неинтуитивное название переменной
    }
    return render(request, "note_edit.html", args)


def note_del(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = Notes.objects.get(id=id, author=auth.get_user(request).id)
    instance.delete()
    return redirect('/') # todo лучше перенаправлять на страницу «заметка успешно удалена»


def addfavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        note = Notes.objects.get(id=id)
        note.favorites = True
        note.save()             # todo лучше через Notes.objects.filter.update
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)


def removefavorites(request, id=None):
    back_url = request.META['HTTP_REFERER']
    try:
        note = Notes.objects.get(id=id)
        note.favorites = False
        note.save()             # todo см выше
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)
