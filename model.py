# Data model and database functions

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions 

class User():
    """User of consensy website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=True)
    lname = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    # groups = db.Relationship()
    # votes = 


class Group():
    """Entity of affiliation between users."""

    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=True)
    # members = 
    # polls = 


class Poll():
    """Proposal or decision to be voted on."""

    __tablename__ = 'polls'

    poll_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=True)
    prompt = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(300))
    # responses = 

    # owner_id = 
    # groups = 
    # votes =


class Vote():
    """A response to a poll submitted by a user."""

    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = 
    # poll_id = 
    # response_id = 


class Response():
    """An expression of agreement or dissent used to respond to a poll."""

    __tablename__ = 'responses'

    response_id = db.Column(db.String(25), primary_key=True)
    description = db.Column(db.String(100), nullable=True)




##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///consensy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
