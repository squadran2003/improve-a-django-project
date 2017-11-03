from django.db import models
from datetime import datetime


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='item')
    created_date = models.DateTimeField(
            default=datetime.now)
    expiration_date = models.DateTimeField(null=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
            default=datetime.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
