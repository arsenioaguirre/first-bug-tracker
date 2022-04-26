from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Bug():
    db = "first_bug_tracker"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.reported_by = db_data['reported_by']
        self.status = db_data['status']
        self.title = db_data['title']
        self.description = db_data['description']
        self.assigned_to = db_data['assigned_to']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']

    @classmethod
    def get_posted_by(cls, data):
        query = "SELECT * FROM bugs JOIN users ON users.id = bugs.user_id WHERE bugs.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            user_bug = cls(row)
            u = {
                'id' : row['users.id'],
                'fname' : row['fname'],
                'lname' : row['lname'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            user_bug.posted_by = User(u)
            print(user_bug.posted_by.fname)
        return user_bug

    @classmethod
    def save(cls, data):
        query = "INSERT INTO bugs (reported_by, status, title, description, assigned_to, user_id) VALUES (%(reported_by)s, %(status)s, %(title)s, %(description)s, %(assigned_to)s, %(user_id)s);"
        return connectToMySQL(cls.db). query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bugs JOIN users ON users.id = bugs.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_bugs = []

        for row in results:
            user_bug = cls(row)
            u = {
                'id' : row['users.id'],
                'fname' : row['fname'],
                'lname' : row['lname'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            user_bug.posted_by = User(u)
            all_bugs.append(user_bug)
            print(user_bug.posted_by.fname)
        return all_bugs

    @classmethod
    def update(cls, data):
        query = "UPDATE bugs SET reported_by=%(reported_by)s, status=%(status)s, title=%(title)s, description=%(description)s, assigned_to=%(assigned_to)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def clear(cls, data):
        query = "DELETE FROM bugs WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_bug(bug):
        is_valid = True
        if len(bug['title']) < 3:
            is_valid = False
            flash("Title must be longer than 3 characters", "bug")
        if len(bug['reported_by']) < 1:
            is_valid = False
            flash("Please include who reported the issue", "bug")
        if len(bug['status']) < 1:
            is_valid = False
            flash("Please include a status", "bug")
        if len(bug['description']) < 3:
            is_valid = False
            flash("Please include a description. At least three characters", "bug")
        if len(bug['assigned_to']) < 0:
            is_valid = False
            flash("Please include an assigned person", "bug")
        return is_valid