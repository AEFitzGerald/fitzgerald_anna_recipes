from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

import re

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.loginpw = data['loginpw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
#self.created_at.strftime("%m-%d-%Y")
    
    @classmethod
    def save_user_in_db(cls,data):
        query = "INSERT INTO users (first_name, last_name, email_address, loginpw) VALUES (%(first_name)s, %(last_name)s,%(email_address)s,%(loginpw)s);"
        
        new_user_account = connectToMySQL("users_recipes_db").query_db(query, data)
        
        return new_user_account
    
    @classmethod
    def get_users_by_email(cls,data):
        query = "SELECT * FROM users WHERE email_address = %(email_address)s;"
        
        results = connectToMySQL("users_recipes_db").query_db(query,data)
        
        users = []
        
        for item in results:
            users.append(User(item))
        
        return users

    @staticmethod
    def validate_user_registration(data):
        is_valid = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        
        if len(data['first_name']) < 2 or len(data['first_name']) > 45:
            flash("First name must contain 2 - 45 characters.")
            is_valid = False
    
        if len(data['last_name']) < 2 or len(data['last_name']) > 45:
            flash("Last name must contain 2 - 45 characters.")
            is_valid = False
        
        if not email_regex.match(data['email_address']):
            flash("Invalid login credentials.")
            is_valid = False
            
        if len(data['loginpw']) < 8:
            flash("Pasword must be at least 8 characters.")
            is_valid = False
        
        if data['loginpw'] != data['confirmpw']:
            flash("Your password needs to match confirm password.")
            is_valid = False
        
        if len(User.get_users_by_email({'email_address': data['email_address']})) != 0:
            flash("This email address is already in use.")
            is_valid = False 
        
        return is_valid