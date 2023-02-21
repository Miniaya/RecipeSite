from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
  name = models.CharField(max_length=200)
  instructions = models.CharField(max_length=400)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Ingredient(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Measurement(models.Model):
  quantity = models.IntegerField(default=1)
  unit = models.CharField(max_length=20)
  recipes = models.ManyToManyField(Recipe)
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
