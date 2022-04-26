from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.bug import Bug
from flask_app.models.user import User

@app.route('/new/bug')
def new_bug():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id" : session['user_id']
    }
    return render_template('new_bug.html', user=User.get_by_id(user_data), users=User.get_all())

@app.route('/create/bug', methods=['POST'])
def create_bug():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bug.validate_bug(request.form):
        return redirect('/new/bug')
    data = {
        "reported_by" : request.form['reported_by'],
        "status" : request.form['status'],
        "title" : request.form['title'],
        "description" : request.form['description'],
        "assigned_to" : request.form['assigned_to'],
        "user_id" : session['user_id']
    }
    Bug.save(data)
    return redirect('/dashboard')

@app.route('/edit/bug/<int:id>')
def edit_bug(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    user_data = {
        "id" : session['user_id']
    }
    return render_template("edit.html", edit=Bug.get_posted_by(data), user=User.get_by_id(user_data), users=User.get_all())

@app.route('/update/bug', methods=['POST'])
def update_bug():
    if 'user_id' not in session:
        return redirect('/logout')
    bug_id = request.form['id']

    if not Bug.validate_bug(request.form):
        return redirect(f'/edit/bug/{bug_id}')

    data = {
        "reported_by" : request.form['reported_by'],
        "status" : request.form['status'],
        "title" : request.form['title'],
        "description" : request.form['description'],
        "assigned_to" : request.form['assigned_to'],
        "id" : request.form["id"]
    }
    Bug.update(data)
    return redirect('/dashboard')

@app.route('/bug/<int:id>')
def show_bug(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    user_data = {
        "id" : session["user_id"]
    }
    return render_template("show_bug.html", bug=Bug.get_posted_by(data), user=User.get_by_id(user_data))

@app.route('/clear/bug/<int:id>')
def clear_bug(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    Bug.clear(data)
    return redirect('/dashboard')


