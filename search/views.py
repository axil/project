from django.contrib import auth
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from notes.models import Notes, Category


def search_form(request):
    return render_to_response('search_form.html', {
        'username': auth.get_user(request).username,
        'category_all': Category.objects.all(),
    })


def search(request):
    if request.GET.get('q'):
        q = request.GET['q']
        args = {
            'username': auth.get_user(request).username,
            'query': q,
            'category_all': Category.objects.all(),
            'notes': Notes.objects.filter(
                (Q(title__icontains=q) | Q(text__icontains=q)) &
                (Q(publish=True) | Q(author=auth.get_user(request))))
            .select_related('category', 'author'),
        }
        return render_to_response('search_results.html', args)
    else:
        return redirect('/')


def filter_title(request):
    if request.GET.get('q'):
        q = request.GET['q']
        args = {
            'username': auth.get_user(request).username,
            'query': q,
            'category_all': Category.objects.all(),
            'notes': Notes.objects.filter(
                Q(title__icontains=q) &
                (Q(publish=True) | Q(author=auth.get_user(request))))
            .select_related('category', 'author'),
        }
        return render_to_response('search_results.html', args)
    else:
        return redirect('/')
