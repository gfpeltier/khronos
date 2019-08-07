import uuid
from enum import Enum
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# TODO: These enums should be customizable
class TaskStatus(Enum):
    TODO = "Not Done"
    DOING = "In Progress"
    DONE = "Complete"


class TaskPriority(Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL = "Critical"


class TaskCategory(Enum):
    HOME = "Home"
    WORK = "Work"
    OTHER = "Other"


# TODO: Create a customizable Add-on so that users can create their own fields
# for tasks
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_created",
        on_delete=models.SET_NULL,
        null=True
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_assigned",
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField(max_length=10000)
    date_created = models.DateTimeField(auto_now_add=True)
    # TODO fields below this should be referenced as possible add-ons
    status = models.CharField(
        max_length=12,
        choices=[(tag.name, tag.value) for tag in TaskStatus],
        default=TaskStatus.TODO
    )
    priority = models.CharField(
        max_length=8,
        choices=[(tag.name, tag.value) for tag in TaskPriority]
    )
    category = models.CharField(
        max_length=5,
        choices=[(tag.name, tag.value) for tag in TaskCategory]
    )
    date_due = models.DateTimeField(null=True, blank=True)
    time_estimate = models.DurationField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    time_wake = models.TimeField()
    time_sleep = models.TimeField()
    time_work_start = models.TimeField()
    time_work_end = models.TimeField()
