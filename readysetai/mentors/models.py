from django.db import models
from enum import Enum

from addons.mixins import TimeStampMixin


class MentorStatus(Enum):
    INVITED = "Invited"
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"


# Create your models here.
class Mentor(TimeStampMixin, models.Model):
    user = models.OneToOneField(
        'users.CustomUser',
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='mentor',
    )
    post = models.CharField(max_length=220, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in MentorStatus],
        default=MentorStatus.INVITED,
    )

    class Meta:
        db_table = 'mentors'
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
