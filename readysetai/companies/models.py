from enum import Enum

from django.db import models

from addons.mixins import TimeStampMixin
from users.models import Roles


class CompanyStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Company(TimeStampMixin, models.Model):
    name = models.CharField(
        max_length=220, unique=True, null=False, blank=False
    )
    description = models.TextField(max_length=3000, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in CompanyStatus],
        default=CompanyStatus.PENDING.value,
    )
    company_admin = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='company_admin',
        limit_choices_to={
            'role__in': [Roles.Company_Admin.name, Roles.Mentor.name]
        },
    )

    class Meta:
        db_table = "companies"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
