from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Recipe, Ingredient, Measurement
from django.contrib.auth.models import User
import sqlite3

@login_required
def index(request):
  user = User.objects.get(username=request.user)
  recipes = Recipe.objects.filter(user=user)
  return render(request, 'recipes/index.html', {'recipe_list': recipes})

# FIX FLAW 2: add login_required annotation and replace recipe with outcommented line
# @login_required
def recipe(request, recipe_id):
  # recipe = get_object_or_404(Recipe, pk=recipe_id, user=User.objects.get(username=request.user))
  recipe = get_object_or_404(Recipe, pk=recipe_id)
  return render(request, 'recipes/recipe.html', {'recipe': recipe})

# FIX FLAW 1: fixes are commented out, also two changes needed in recipe.html
@login_required
def add_ingredient(request, recipe_id):
  recipe = get_object_or_404(Recipe, pk=recipe_id)
  try:
    added_ingredient = Ingredient.objects.get_or_create(
      name=request.GET.get('name'), # name=request.POST.get('name'),
    )
    added_measurement = Measurement.objects.get_or_create(
      quantity=int(request.GET.get('quantity')), # quantity=int(request.POST.get('quantity')),
      unit=request.GET.get('unit'), # unit=request.POST.get('unit'),
      ingredient=added_ingredient[0]
    )
    recipe.measurement_set.add(added_measurement[0])
  except (ValueError):
    return render(request, 'recipes/recipe.html', {
          'recipe': recipe,
          # FIX FLAW 5: Replace error_message with
          # 'error_message': 'Wrong value type, check your input',
          'error_message': 'Something went wrong, please investigate:\n' + request.method + ' ' + request.path + '\n' + str(request.COOKIES) + '\n' + str(request.session),
        })
  else:
    return HttpResponseRedirect(reverse('recipes:recipe', args=(recipe.id,)))

@login_required
def add_instructions(request, recipe_id):
  recipe = get_object_or_404(Recipe, pk=recipe_id)
  recipe.instructions = request.POST['instructions']
  recipe.save()
  return HttpResponseRedirect(reverse('recipes:recipe', args=(recipe.id,)))

@login_required
def new(request):
  added_recipe = Recipe.objects.get_or_create(
    name=request.POST['name'],
    user=User.objects.get(username=request.user)
  )
  return HttpResponseRedirect(reverse('recipes:index'))

@login_required
def search(request):
  user = User.objects.get(username=request.user)
  #FIX FLAW 3: replace lines 66-71 with
  # recipes = Recipe.objects.filter(user=user, name__icontains=request.GET['keyword'])
  connection = sqlite3.connect('recipes.db')
  cursor = connection.cursor()
  response = cursor.execute("SELECT * FROM recipes_recipe WHERE user_id='%s' and name LIKE '%%%s%%'" % (user.id, request.GET['keyword'])).fetchall()
  recipes = []
  for recipe in response:
    recipes.append({'id': recipe[0], 'name': recipe[1]})
  return render(request, 'recipes/index.html', {'recipe_list': recipes})