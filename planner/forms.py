from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Task


class TaskCreationForm(ModelForm):
    """Form that creates a task for logged in user as the creator
    """
