from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # SAVE
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users 
        (first_name, last_name, email, password, created_at, updated_at) 
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # GET ALL

    @classmethod
    def getAll(cls):
        query = " SELECT * FROM users JOIN recipes ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    # GET BY EMAIL
    @classmethod
    def getOne_ByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])  # Don't foget to bring the first row !

    # GET BY ID
    @classmethod
    def getOne_ById(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        # If it is NOT matched => Can not log in!!! False
        return cls(result[0])

    # DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_user(data):
        is_valid = True

        # Check no empty input
        if len(data['first_name']) < 1 or len(data['last_name']) < 1 or len(data['email']) < 1:
            flash("Please fill out your informtaion", "register")
            is_valid = False

        # Check right email format
        if len(data['email']) > 1 and not EMAIL_REGEX.match(data['email']):
            flash("Invalid email format!", "register")
            is_valid = False

        # Check passwords are matched
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False

        if data['password'] == '':
            flash("Please enter password", "register")
            is_valid = False
        return is_valid
