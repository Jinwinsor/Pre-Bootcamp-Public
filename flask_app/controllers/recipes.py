from flask_app import app
from flask import render_template, redirect, request, session, flash
import re
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ======== DASHBOARD ============  AFTER log-in page
@app.route('/recipes_dash')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user')

    # Display all recipes on the page for the user(Only One user) | After login, it has to be session id.
    data = {
        'id': session['user_id']
    }

    this_user = User.getOne_ById(data)  # users.id = recipes.user_id

    if not this_user:
        return redirect('/logout')

    return render_template('dashboard.html', user=User.getOne_ById(data), recipes=Recipe.getAll())


# ========= Recipe CREATE PAGE =========


@app.route('/recipes/create')
def create():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('create_recipe.html')


@app.route('/recipes/create/new', methods=['POST'])
def create_new():

    if not Recipe.vadlidate_recipe(request.form):
        return redirect('/recipes/create')

    if 'user_id' not in session:
        return redirect('/user')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30']
    }
    print(data)

    Recipe.save(data)
    flash("The recipe is created!", "success")
    return redirect('/recipes_dash')


# ============ EDIT PAGE ============

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/user')
    data = {
        'id': id
    }
    # Brings One ID for ediing
    return render_template('edit_recipe.html', recipe=Recipe.getOne_byId(data))


@app.route('/recipes/edit/update/<int:id>', methods=['POST'])
def update_edit(id):
    if 'user_id' not in session:
        return redirect('/user')
    if not Recipe.vadlidate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
    }
    Recipe.update(data)
    return redirect('/recipes_dash')


# Detail page


@app.route('/recipes/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/user')

    data = {
        'id': id
    }

    this_recipe = Recipe.getOne_byId(data)
    # this_user = User.getOne_ById(data)
    return render_template('view_recipe.html', recipe=this_recipe)

# ====== Delete ========


@app.route('/recipes/delete/<int:id>')
def delete(id):

    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/recipes_dash')
