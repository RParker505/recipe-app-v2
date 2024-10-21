from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe    #to access Recipe model
from .forms import AddRecipeForm

# Create your tests here.
class RecipeModelTest(TestCase):

    # Define test data to initialize variables in test database
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(name='Tea', cooking_time=5, ingredients='tea-leaves, water, sugar')

    # Test if recipe name is initialized as expected
    def test_recipe_name(self):
       # Get a recipe object to test
       recipe = Recipe.objects.get(id=1)

       # Get the metadata for the 'name' field and use it to query its data
       recipe_name_label = recipe._meta.get_field('name').verbose_name

       # Compare the value to the expected result
       self.assertEqual(recipe_name_label, 'name')

    # Test that recipe name is a max of 120 characters
    def test_recipe_name_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('name').max_length

        # Compare the value to the expected result i.e. 400
        self.assertEqual(max_length, 120)

    # Test that ingredients is a max of 400 characters
    def test_ingredients_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('ingredients').max_length

        # Compare the value to the expected result i.e. 400
        self.assertEqual(max_length, 400)

    # Test that cooking_time is an integer
    def test_cooking_time_integer(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'cooking_time' field and use it to query its type
        cooking_time = recipe.cooking_time

        # Assert that cooking_time is a whole number (integer-like)
        self.assertTrue(cooking_time.is_integer(), "Cooking time is not an integer")

    # Test that difficulty is accurately calculated
    def test_difficulty_calc(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Assert the difficulty is calculated accurately
        self.assertEqual(recipe.calculate_difficulty(), 'Easy')

    # Test that absolute URL is correctly generated and that the RecipeDetailView loads with name is clicked
    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absolute_url() should take you to the detail page of recipe #1 and load the URL recipes/list/1
        self.assertEqual(recipe.get_absolute_url(), '/recipes/1')

class RecipeFormTests(TestCase):

    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create some test recipes
        Recipe.objects.create(name="Pasta", cooking_time=30, ingredients="Tomato, Pasta")
        Recipe.objects.create(name="Salad", cooking_time=10, ingredients="Lettuce, Tomato, Cucumber")

    def test_login_required(self):
        """Test that the search view is login-protected."""
        response = self.client.get(reverse('recipes:recipe_search'))  # No namespace needed
        self.assertNotEqual(response.status_code, 200)  # Should redirect if not logged in
        self.assertRedirects(response, '/login/?next=/search/')  # Now it reflects the '/search/' path

    def test_page_loads_after_login(self):
        """Test that the search page loads after the user logs in."""
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get(reverse('recipes:recipe_search'))  # No namespace needed
        self.assertEqual(response.status_code, 200)  # Check if page loads
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')  # Check if correct template is used

    def test_form_submission_filters_recipes(self):
        """Test that the form filters recipes by name."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipes:recipe_search'), {'Recipe_Name': 'Pasta'})
        
        # Check if only the "Pasta" recipe is in the response context
        self.assertContains(response, 'Pasta')
        self.assertNotContains(response, 'Salad')  # Ensure other recipes are filtered out

    def test_form_chart_generation(self):
        """Test that the chart is generated when a valid chart type is selected."""
        self.client.login(username='testuser', password='testpass')
        
        # Post a request with valid data for chart generation
        response = self.client.post(reverse('recipes:recipe_search'), {
            'Recipe_Name': 'Pasta',
            'chart_type': '#2',  # Use the correct key for pie chart (matching the form's CHART_CHOICES)
        })
        
        # Check if chart is in the context and is not None
        self.assertIn('chart', response.context)  # Check if 'chart' key exists in the context
        self.assertIsNotNone(response.context['chart'])  # Ensure a chart is actually generated

    def test_form_invalid_submission(self):
        """Test that an invalid form submission doesn't break the view."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipes:recipe_search'), {'chart_type': 'invalid_chart'})
        self.assertEqual(response.status_code, 200)  # Page should still load
        self.assertIsNone(response.context.get('chart'))  # No chart should be generated with invalid data

class AddRecipeFormTests(TestCase):

    def test_valid_form(self):
        """Test if the form is valid when given valid data"""
        form_data = {
            'name': 'Chocolate Cake',
            'cooking_time': 45.0,
            'ingredients': 'flour, sugar, cocoa powder, eggs',
            'pic': None  # Assuming the image is optional
        }
        form = AddRecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        """Test if the form is invalid when 'name' is missing"""
        form_data = {
            'cooking_time': 45.0,
            'ingredients': 'flour, sugar, cocoa powder, eggs',
            'pic': None
        }
        form = AddRecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_invalid_form_empty_ingredients(self):
        """Test if the form is invalid when 'ingredients' is an empty string"""
        form_data = {
            'name': 'Chocolate Cake',
            'cooking_time': 45.0,
            'ingredients': '',  # Invalid empty ingredients
            'pic': None
        }
        form = AddRecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ingredients', form.errors)

    def test_form_invalid_cooking_time(self):
        """Test if form is invalid with non-float cooking time"""
        form_data = {
            'name': 'Pasta',
            'cooking_time': 'invalid_time',  # Invalid time
            'ingredients': 'pasta, sauce',
            'pic': None
        }
        form = AddRecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors)

class AboutMeViewTests(TestCase):

    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_about_me_view_status_code(self):
        """Test if About Me view returns a 200 status code"""
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get(reverse('recipes:about_me'))
        self.assertEqual(response.status_code, 200)

    def test_about_me_template_used(self):
        """Test if the correct template is used for About Me view"""
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get(reverse('recipes:about_me'))
        self.assertTemplateUsed(response, 'recipes/about_me.html')

    def test_about_me_content(self):
        """Test if the About Me page contains expected content"""
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get(reverse('recipes:about_me'))
        self.assertContains(response, "Rocky")  # Check that my name header is there
        self.assertContains(response, "Bon appetit!")   # A portion of the bio
        self.assertContains(response, "Technology Used")     # Check if 'Skills' section is there