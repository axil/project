from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib import auth

from notes.models import Notes

# Create your views here.
def hello(request):
    args = {}
    return render_to_response('notes.html', args)


def notes(request, page_number=1):
    args = {}
    args['notes'] = Notes.objects.order_by('-date')
    args['username'] = auth.get_user(request).username
    return render_to_response('notes.html', args)

def note(request, id=None):
    args = {}
    args['note'] = Notes.objects.get(id=id)
    args['username'] = auth.get_user(request).username
    return render_to_response('note.html', args)



# def article(request, article_id=1):
#     args = {}
#     args.update(csrf(request))
#     args['article'] = Article.objects.get(id=article_id)
#     args['username'] = auth.get_user(request).username
#     args['form'] = CommentForm
#     args['comments'] = Comment.objects.filter(comment_article=article_id)
#     args['projects'] = Category.objects.all()
#     return render_to_response('article.html', args)
