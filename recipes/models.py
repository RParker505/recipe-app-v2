from django.db import models
from django.shortcuts import reverse

# Create your models here.

# Define class(table) and inherit from models.Model for basic functionality and attributes
class Recipe(models.Model):

    # Define attributes/columns in the table
    name= models.CharField(max_length=120)
    cooking_time= models.FloatField(help_text='minutes')
    ingredients= models.CharField(max_length=400, help_text='Ingredients must be separated by commas.')
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    # Calculate recipe difficulty
    def calculate_difficulty(self):
        ing_list = self.ingredients.split(', ')
        num_ingredients = len(ing_list)
        if self.cooking_time < 10:
            if num_ingredients < 4:
                difficulty = 'Easy'
            else:
                difficulty = 'Medium'
        else:
            if num_ingredients < 4:
                difficulty = 'Intermediate'
            else:
                difficulty = 'Hard'
        return difficulty

    # Define string representation and the parameter you want to use to refer to the recipe
    def __str__(self):
        return str(self.name)

    # Take primary key as an argument and generate a URL
    def get_absolute_url(self):
        return reverse ('recipes:detail', kwargs={'pk': self.pk})