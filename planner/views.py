from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Task, TaskPriority, TaskCategory
from .forms import TaskCreationForm


@login_required(login_url="/login/")
def dashboard(request):
    try:
        utasks = Task.objects.filter(assignee=request.user)
    except Task.DoesNotExist:
        utasks = None
    template = loader.get_template("planner/dashboard.html")
    context = {
        'user': request.user,
        'tasks': utasks,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        context = {
            'priority_opts': [(tag.name, tag.value) for tag in TaskPriority],
            'category_opts': [(tag.name, tag.value) for tag in TaskCategory],
            'form': form
        }
        if form.is_valid():
            utask = form.save()
            utask.creator = request.user
            utask.assignee = request.user
            utask.save()
            return redirect('/planner/dashboard')
    else:
        form = TaskCreationForm()
        context = {
            'priority_opts': [(tag.name, tag.value) for tag in TaskPriority],
            'category_opts': [(tag.name, tag.value) for tag in TaskCategory],
            'form': form
        }
    return render(request, 'planner/new_task.html', context)


@login_required(login_url="/login/")
def create_user_profile(request):
    # TODO
    pass


@login_required(login_url="/login/")
def task_details(request, slug=None):
    utask = get_object_or_404(Task, id=slug)
    template = loader.get_template('planner/task_details.html')
    return HttpResponse(template.render({'task': utask}, request))
