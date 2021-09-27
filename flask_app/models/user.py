# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# Now we use class methods to query our database
    @staticmethod
    def validate_info(data):
        result = True
        query = "SELECT * FROM users WHERE email = %(email)s ;"
        if not len(data['first_name']) >= 3:
            result= False
            flash("The first name must be at least three characters long")
        if not len(data['last_name']) >=3:
            result = False
            flash("The last name must be at least three characters long")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            result = False
        if len(connectToMySQL('users').query_db(query,data)) >0:
            result=False
            flash("This email is already registered in our database")
        return result
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def get_user_info(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        user = connectToMySQL('users').query_db(query,data)
        return user
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users').query_db( query, data )
    @classmethod
    def update(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s , last_name = %(last_name)s, email = %(email)s , updated_at = NOW() WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users').query_db( query, data )
    @classmethod
    def remove(cls, data ):
        # query = "SET SQL_SAFE_UPDATES = 0;"
        query = "DELETE FROM users WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users').query_db( query, data )