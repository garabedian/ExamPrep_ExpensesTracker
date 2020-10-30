from django.db import models
from main.validators import budget_validator, availability_validator


class Profile(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=100, default="")
    budget = models.IntegerField(default=0, validators=[budget_validator])  # Model validation


class Expenses(models.Model):
    title = models.CharField(max_length=50)
    image_url = models.URLField(default='')
    description = models.TextField(default='')
    price = models.FloatField(default=0, validators=[budget_validator, availability_validator])
