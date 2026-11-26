from django.db import models
from addons.mixins import TimeStampMixin
from mentors.models import Mentor
from enum import Enum


class NewcomerStatus(Enum):
    INVITED = "Invited"
    LEARNING = "Learning"
    REVIEW = "Readiness Review"
    BLOCKED = "Blocked"
    READY = "Ready"


class Newcomer(TimeStampMixin):
    user = models.OneToOneField(
        'users.CustomUser', on_delete=models.CASCADE, related_name='newcomer'
    )
    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newcomers',
    )
    post = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(
        max_length=50,
        choices=[(status.value, status.name) for status in NewcomerStatus],
        default=NewcomerStatus.INVITED.value,
    )
    start_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Newcomer'
        verbose_name_plural = 'Newcomers'
        db_table = 'newcomers'

    def __str__(self):
        return self.name
