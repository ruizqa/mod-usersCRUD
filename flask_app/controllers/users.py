from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User



@app.route("/")
def form():
    return render_template("create.html")


@app.route('/create', methods=["POST"])
def create_user():

    data = {
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"]
    }
    if not User.validate_info(data):
        return redirect("/")

    User.save(data)

    return redirect('/users')            

@app.route("/users")
def read():

    users = User.get_all()
    return render_template("read.html", users=users)

@app.route("/users/<int:id>")
def show_user(id):
    data = {
        'id': id,
        
    }
    user=User.get_user_info(data)
    user.created_at = user.created_at.strftime("%B %d, %Y ")
    user.updated_at = user.updated_at.strftime("%B %d, %Y at %I:%M %p")
  
    return render_template("show_user.html", user=user)

@app.route("/users/<int:id>/edit")
def edit_user(id):
    data = {
        'id': id
    }
    user=User.get_user_info(data)

    session['id'] = id
    return render_template("edit.html", user=user)

@app.route('/update', methods=["POST"])
def update_user():

    print("El request es", request.form)
    data = {
        'id': session['id'],
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"]
    }

    User.update(data)

    return redirect(f"/users/{session['id']}")  


@app.route("/users/<int:id>/destroy")
def destroy(id):
    data={
        'id': id
    }

    User.remove(data)
    
    return redirect('/users')
