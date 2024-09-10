"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class AddPetForm(FlaskForm):
    """Form for adding pets, with breed and special needs fields."""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine"), ("rabbit", "Rabbit")])
    breed = StringField("Breed", validators=[Optional()])  # New field
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    special_needs = TextAreaField("Special Needs", validators=[Optional()])  # New field


class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    special_needs = TextAreaField("Special Needs", validators=[Optional()])  # New field
    status = SelectField("Status", choices=[("Available", "Available"), ("Pending", "Pending"), ("Adopted", "Adopted")])
