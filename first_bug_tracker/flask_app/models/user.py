from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import bug

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User():
    db = "first_bug_tracker"
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash('Email is already in use', 'register')
            is_valid = False
        if len(user['fname']) < 2:
            flash('First name must be at least 2 characters', 'register')
            is_valid = False
        if len(user['lname']) < 2:
            flash('Last name must be at least 2 characters', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Password and Confirm Password do not match', 'register')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(fname, lname, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])