import uuid
from enum import Enum
from django.db import models
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
        User,
        related_name="user_created",
        on_delete=models.SET_NULL,
        null=True
    )
    assignee = models.ForeignKey(
        User,
        related_name="user_assigned",
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=10000)
    date_created = models.DateTimeField(auto_now_add=True)
    # TODO fields below this should be referenced as possible add-ons
    status = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in TaskStatus]
    )
    priority = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in TaskPriority]
    )
    category = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in TaskCategory]
    )
    date_due = models.DateTimeField(blank=True)
    time_estimate = models.DurationField(blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    time_wake = models.TimeField()
    time_sleep = models.TimeField()
    time_work_start = models.TimeField()
    time_work_end = models.TimeField()
