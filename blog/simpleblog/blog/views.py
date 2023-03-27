from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def home(request):
    return render(request, 'blog/index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'blog/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'blog/signup.html', {'form': UserCreationForm(),
                                                            'error': 'This username already exists, try another',
                                                            })
        else:
            return render(request, 'blog/signup.html', {'form': UserCreationForm(),
                                                        'error': 'Passwords mismatch',
                                                        })


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'blog/signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'blog/signin.html', {'form': AuthenticationForm(),
                                                        'error': 'Invalid data, try again',
                                                        })
        else:
            login(request, user)
            return redirect('index')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signin')


def tools(request):
    articles = Article.objects.order_by('-date')
    return render(request, 'blog/tools.html', {'articles': articles})
