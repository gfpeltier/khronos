from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Task, TaskPriority, TaskCategory


@login_required(login_url="/login/")
def dashboard(request):
    try:
        utasks = Task.objects.get(assignee=request.user)
    except Task.DoesNotExist:
        utasks = None
    template = loader.get_template("planner/dashboard.html")
    context = {
        'tasks': utasks,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def create_task(request):
    if request.method == 'GET':
        template = loader.get_template('planner/new_task.html')
        context = {
            'priority_opts': [(tag.name, tag.value) for tag in TaskPriority],
            'category_opts': [(tag.name, tag.value) for tag in TaskCategory],
        }
        return HttpResponse(template.render(context, request))
    else:
        # TODO: Form validation
        pass


@login_required(login_url="/login/")
def create_user_profile(request):
    # TODO
    pass


@login_required(login_url="/login/")
def task(request):
    # TODO
    pass
