"""Models for adopt app."""

from flask_sqlalchemy import SQLAlchemy

GENERIC_IMAGE = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"

db = SQLAlchemy()


class Pet(db.Model):
    """Adoptable pet with additional fields for uniqueness."""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    breed = db.Column(db.Text)  # New field
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    special_needs = db.Column(db.Text)  # New field for special care instructions
    status = db.Column(db.Text, nullable=False, default="Available")  # Replacing the "available" field

    def image_url(self):
        """Return image for pet -- bespoke or generic."""
        return self.photo_url or GENERIC_IMAGE


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)
