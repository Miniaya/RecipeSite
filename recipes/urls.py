from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
  path('', views.index, name='index'),
  path('new/', views.new, name='new'),
  path('search/', views.search, name='search'),
  path('<int:recipe_id>/', views.recipe, name='recipe'),
  path('<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
  path('<int:recipe_id>/add_instructions/', views.add_instructions, name='add_instructions')
]