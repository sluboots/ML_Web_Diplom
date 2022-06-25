from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from user.models import Profile
import uuid


class Vacancy(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    resume = models.TextField(blank=False, verbose_name='Резюме')
    cluster = models.IntegerField(blank=True, verbose_name= 'Кластер', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


class Resume(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    vacancy = models.TextField(blank=False, verbose_name='Вакансия')
    cluster = models.IntegerField(blank=True, verbose_name= 'Кластер', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


# Create your models here.
