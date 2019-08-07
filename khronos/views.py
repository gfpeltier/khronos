from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/planner/dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'khronos/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('/planner/dashboard')
        else:
            context = {'errors': ['Incorrect username or password']}
            template = loader.get_template('khronos/login.html')
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('khronos/login.html')
        return HttpResponse(template.render(None, request))


@login_required(login_url="/login/")
def user_signout(request):
    logout(request)
    return redirect('/login')
