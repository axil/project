from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from notes.models import Notes, Category


def search_form(request):
    return render_to_response('search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:                         # todo лучше request.GET.get('q')
        q = request.GET['q']
        args = {
            'username': auth.get_user(request).username,
            'query': request.GET['q'],
            'projects': Category.objects.all(),
            'notes': Notes.objects.filter(
                (Q(title__icontains=q) | Q(text__icontains=q))&
                (Q(publish=True) | Q(author=auth.get_user(request).id))).       
            # todo лучше либо author_id=auth.get_user(request).id либо author=auth.get_user(request)
                select_related('category','author'),
        }
        return render_to_response('search_results.html', args)
    else:
        return HttpResponse('Please submit a search term.')

def fillter_title(request):           # todo двойная l
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        args = {
            'username': auth.get_user(request).username,
            'query': request.GET['q'],
            'projects': Category.objects.all(),
            'notes': Notes.objects.filter(Q(title__icontains=q)&
                (Q(publish=True) | Q(author=auth.get_user(request).id))).
                select_related('category','author'),
        }
        return render_to_response('search_results.html', args)
    else:
        return HttpResponse('Please submit a search term.')       
    # todo для юзера не интуитивно что делать дальше. Хотя бы сделайте ссылку на главную страницу,
    # а вообще это делается через messages
