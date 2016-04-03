from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from notes.models import Notes, Category
from loginsys.forms import RegistrationForm


def login(request):
    args = {}
    args.update(csrf(request))

    args['projects'] = Category.objects.all()
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}

    args['projects'] = Category.objects.all()
    args.update(csrf(request))
    args['form'] = RegistrationForm()
    if request.POST:
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            new_user = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                         password=newuser_form.cleaned_data['password2'])
            auth.login(request, new_user)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
