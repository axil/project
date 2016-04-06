from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from notes.models import Notes, Category


def search_form(request):
    return render_to_response('search_form.html')


def search(request):
    args ={}
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        args = {
            'username': auth.get_user(request).username,
            'query': request.GET['q'],
            'projects': Category.objects.all(),
            'notes': Notes.objects.filter((Q(title__icontains=q) | Q(text__icontains=q))&
                                          (Q(publish=True) | Q(author=auth.get_user(request).id))).
            select_related('category','author'),
        }

        # args['query'] = request.GET['q']
        # args['category'] = Category.objects.all()
        # q = request.GET['q']
        # args['notes'] = Notes.objects.filter(title=q)
        return render_to_response('search_results.html', args)
    else:
        return HttpResponse('Please submit a search term.')
# Q(user = None) | Q(user = User)