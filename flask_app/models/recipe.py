from flask_app import app
from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models.user import User

class Recipe():
    
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.thirty_minutes_y_n = data['thirty_minutes_y_n']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def add_recipe(cls,data):
        
        query = "INSERT INTO recipes (title, description, instructions, date, thirty_minutes_y_n, user_id) VALUES (%(title)s, %(description)s, %(instructions)s, %(date)s, %(thirty_minutes_y_n)s, %(user_id)s);"
        
        new_recipe_id = connectToMySQL("users_recipes_db").query_db(query, data)
        
        
        return new_recipe_id

    @classmethod
    def get_all_recipes(cls):
        
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        
        results = connectToMySQL("users_recipes_db").query_db(query)
        
        recipes = []
        
        for item in results:
            recipe = cls(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email_address': item['email_address'],
                'loginpw': item['loginpw'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
                }
            recipe.user = User(user_data)
            recipes.append(recipe)
        
        return recipes
        
    @classmethod
    def get_recipe_by_id(cls,data):
        
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        
        result = connectToMySQL("users_recipes_db").query_db(query, data)
        
        recipe = cls(result[0])
        user_data = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email_address': result[0]['email_address'],
                'loginpw': result[0]['loginpw'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
                }
        recipe.user = User(user_data)
        return recipe
    
    @classmethod
    def update_recipe(cls, data):
        
        query = 'UPDATE recipes SET title = %(title)s, description = %(description)s, instructions = %(instruction)s, date = %(date)s, thirty_minutes_y_n = %(thirty_minutes_y_n)s  WHERE id = %(id)s;'

        connectToMySQL("users_recipes_db").query_db(query, data)
    
    @classmethod
    def delete_recipe(cls,data):
    
        query = 'DELETE FROM recipes WHERE id = %(id)s;'

        connectToMySQL("users_recipes_db").query_db(query, data)
        
    @staticmethod
    def validate_recipe(data):
            is_valid = True
            
            if len(data['title']) < 3 or len(data['title']) > 45:
                flash("Title name must contain 2 - 45 characters.")
                is_valid = False
        
            if len(data['description']) < 3 or len(data['description']) > 255:
                flash("Description must contain 2 - 255 characters.")
                is_valid = False
            
            if len(data['instructions']) < 3 or len(data['instructions']) > 1000:
                flash("Instructions must contain 3 -1000 characters.")
                is_valid = False 
            
            if len(data['date']) == 0:
                flash("Please enter a date.")
                is_valid = False
                
            if len(data['thirty_minutes_y_n']) < 2 or len(data['thirty_minutes_y_n']) > 3:
                flash("You must check yes or no.")
                is_valid = False 
            
            return is_valid
