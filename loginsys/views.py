from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from notes.models import Notes, Category
from loginsys.forms import RegistrationForm


def login(request):
    args = {}
    args.update(csrf(request))
    args['category_all'] = Category.objects.all()
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


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {
        'category_all': Category.objects.all(),
        'form': RegistrationForm(),
    }
    args.update(csrf(request))
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
