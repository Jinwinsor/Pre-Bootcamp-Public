from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import recipe
import re

# Don't forget to add 'user_id' inside the save!


class Recipe:
    db = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None  # User instance

    # SAVE

    @classmethod
    def save(cls, data):     # Don't forget to add 'user_id' inside the save!
        query = """
        INSERT INTO recipes
        (name, description, instructions, date_made, under_30, user_id)
        VALUES
        (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # getAll
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        # this_recipe = None  # There is no recipe at the first time (Don't use this!)
        for row in results:
            this_recipe = cls(row)
            # if this_recipe == None:
            #     this_recipe = cls(row)
            # if not this_recipe == row['id']:
            #     # Put 'this_recipe' in 'all_recipes'.
            #     recipes.append(this_recipe)
            #     this_recipe = cls(row)

    # I thought above code is correct. But it wasn't. It shows multiple results!

            if row['user_id'] == None:    # user_id = recipes.user_id
                break                     # recipes 에 아무것도 없으면 멈춰라
            data = {                      # recipes 에 포스팅이 올라왔다면, 새로운 포스팅에 맞는 유저(this_recipe.owner)를 만들어라.
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            # OWNER = 새로 업데이트된 데이터를 가진 owner가  this_recipe를 가지고있다.
            this_recipe.owner = user.User(data)
            # user instance에 이 새로 업데이트된 데이터를 넣어 새 유저가 가진 this_recipe
            recipes.append(this_recipe)
        return recipes

    # getOne_byId
    @classmethod
    def getOne_byId(cls, data):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)  # For checking the result.
        # if results:
        #     # Bring one on the top ! We need only One ID.
        #     return cls(results[0])
        this_recipe = cls(results[0])  # Only one  on the top!

# get_all 에서는 this_recipe = cls(row)
# get_by_one 에서는 this_recipe = cls(results[0])  ==> row = results[0]

        row = results[0]
        data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        # Every recipe has its own owner. Obly the person can edit the recipe.
        this_recipe.owner = user.User(data)
        return this_recipe

    # Update

    @classmethod
    def update(cls, up_data):
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s , date_made = %(date_made)s, under_30 = %(under_30)s
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, up_data)
        return results

    # Delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


# ====== Recipe Validation Form ======


    @staticmethod
    def vadlidate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 charactors", "error")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3  charactors", "error")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 charactors", "error")
            is_valid = False
        if recipe['date_made'] == '':
            flash("Please fill out the date", "error")
            is_valid = False
        if 'under_30' not in recipe:
            flash("Please pick one. Yes or No?", "error")
            is_valid = False
        return is_valid
