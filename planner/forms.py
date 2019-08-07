from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .models import Task, TaskCategory, TaskPriority


class TaskCreationForm(ModelForm):
    """Form that creates a task for logged in user as the creator
    """
    err_msgs = {
        'bad_category': _("Category selected does not exist"),
        'bad_priority': _("Priority selected does not exist"),
    }

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'priority',
            'category',
            'date_due',
            'time_estimate'
        ]

    def clean_category(self):
        category = self.cleaned_data['category']
        category = TaskCategory[category]
        if category is None:
            raise forms.ValidationError(
                self.err_msgs['bad_category'],
                code='bad_category',
            )
        return category.name

    def clean_priority(self):
        prio = self.cleaned_data['priority']
        prio = TaskPriority[prio]
        if prio is None:
            raise forms.ValidationError(
                self.err_msgs['bad_priority'],
                code='bad_priority',
            )
        return prio.name

    def save(self, commit=True):
        task = super(TaskCreationForm, self).save(commit=False)
        task.slug = slugify(task.title)
        if commit:
            task.save()
        return task
