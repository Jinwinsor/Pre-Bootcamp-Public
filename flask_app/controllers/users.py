from flask_app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, session, flash
import re
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ======== BASIC HOME =========
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def home():
    return redirect('/')

# ======= RESITER ===============


@app.route('/user/register', methods=['POST'])
def register():
    # Check it's right register form?
    if not User.validate_user(request.form):
        return redirect('/user')

    # Check the password form
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    print(data)

    # Save the new inform from a user and save the data
    user_id = User.save(data)
    session['user_id'] = user_id

    flash("You are logged in!", "success")
    return redirect('/recipes_dash')

# ======== LOG IN ============================= #


@app.route('/user/login', methods=['POST'])
def login():

    # Let login through email.
    # Take ONE through the email
    data = {
        'email': request.form['email']
    }

    # (1)Email check
    user = User.getOne_ByEmail(data)

    if not user:
        flash("Invalid email", "login")
        return redirect('/user')

    # (2)Password check
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password", "login")
        return redirect('/user')

    session['user_id'] = user.id

    if 'user_id' in session:
        return redirect('/recipes_dash')  # Success => go to dashboard

 #  ======= LOG OUT =========


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/user')
