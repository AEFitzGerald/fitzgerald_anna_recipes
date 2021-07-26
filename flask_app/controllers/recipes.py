from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/dashboard')
def dashboard_recipes():
    if 'id' not in session:
        flash("Hi! Please log in to view this page.")
        return redirect('/')
    
    recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', recipes = recipes)

@app.route('/recipes/new')
def recipes_new():
    
    if 'id' not in session:
        flash("Hi! Please log in to view this page.")
        return redirect('/')
        
    return render_template('recipes_new.html')

@app.route('/submit_new_recipe', methods=['POST'])
def submit_new_recipe():
    if Recipe.validate_recipe(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date': request.form['date'],
            'thirty_minutes_y_n': request.form['thirty_minutes_y_n'],
            "user_id" : session['id']
            }
        Recipe.add_recipe(data)
        print('recipe valid')
        return redirect('/dashboard')
    print('recipe invalid')
    return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods = ['POST'])
def update_recipe(recipe_id):
    if Recipe.validate_recipe(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date': request.form['date'],
            'thirty_minutes_y_n': request.form['thirty_minutes_y_n'],
            "user_id" : session['id']
        }
        Recipe.update_recipe(data)
        return redirect(f'/paintings/{recipe_id}')

@app.route('/recipes/<int:recipe_id>/instructions')
def instructions(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('instructions.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/delete')
def delete_painting(recipe_id):

    Recipe.delete_recipe({'id': recipe_id })

    return redirect('/dashboard')


