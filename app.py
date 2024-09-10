"""Flask app for adopt app."""

import os
from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use the loaded SECRET_KEY from .env or fallback to a default for local development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect the database to the Flask app
connect_db(app)

# Create database tables in the proper application context
with app.app_context():
    db.create_all()

# Initialize the Debug Toolbar
toolbar = DebugToolbarExtension(app)


##############################################################################
# Routes

@app.route("/")
def list_pets():
    """List all pets grouped by their availability status."""

    available_pets = Pet.query.filter_by(status="Available").all()
    pending_pets = Pet.query.filter_by(status="Pending").all()
    adopted_pets = Pet.query.filter_by(status="Adopted").all()

    return render_template("pet_list.html", 
                           available_pets=available_pets, 
                           pending_pets=pending_pets, 
                           adopted_pets=adopted_pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a new pet."""
    
    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_pets'))

    return render_template("pet_add_form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit an existing pet's details."""
    
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.special_needs = form.special_needs.data
        pet.status = form.status.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about a pet in JSON."""
    
    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age, "status": pet.status}
    
    return jsonify(info)


# Main entry point for running the app
if __name__ == "__main__":
    app.run(debug=True)
