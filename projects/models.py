from django.conf import settings
from django.db import models

from projects.constants import PROJECT_NAME_MAX_LENGTH
from team_finder.validators import validate_github_url


class Project(models.Model):

    class Status(models.TextChoices):
        OPEN = "open", "Открыт" 
        CLOSED = "closed", "Закрыт" 

    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    github_url = models.URLField(
        blank=True, verbose_name="GitHub", validators=[validate_github_url],
    )
    status = models.CharField(
        max_length=max(len(s) for s in Status.values),
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participating_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
