"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    """redirect to list of users"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show add user button."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/new")
def show_add_user_form():
    """Show an add form for users"""
    return render_template("create_user.html")


@app.route("/users/new", methods=["POST"])
def process_add_form():
    """Process add form for new users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show user edit form."""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user(user_id):
    """process user edit form."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # user = User(first_name=first_name,
                # last_name=last_name, image_url=image_url)
    user = User.query.get_or_404(user_id)  # why are we defining users twice?
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
