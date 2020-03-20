# Data model and database functions

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions
class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    """User of consensy website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} name={self.fname} {self.lname}>"


class Group(ModelMixin, db.Model):
    """Entity of affiliation between users."""

    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Group group_id={self.group_id} name={self.name}>"


class UserGroup(ModelMixin, db.Model):
    """Association table linking User and Group."""

    __tablename__ = 'usergroup'

    usergroup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    user = db.relationship('User', backref='groups')
    group = db.relationship('Group', backref='members')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserGroup id={self.usergroup_id} user={self.user_id} group={self.group_id}>"


class Poll(ModelMixin, db.Model):
    """Proposal or decision to be voted on."""

    __tablename__ = 'polls'

    poll_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    owner = db.relationship('User', backref='admin')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Poll poll_id={self.poll_id} {self.title}>"

    def tally_results(self):
        """Tally each vote by response. Return a dictionary."""

        results = {'agr': 0,
                   'rsv': 0,
                   'asd': 0,
                   'blk': 0}

        print(f'Results initialized: {results}')

        responses = ['agr', 'rsv', 'asd', 'blk']

        for vote in self.votes:
            for response in responses:
                if vote.response == response:
                    results[response] += 1

        return results


class GroupPoll(ModelMixin, db.Model):
    """Association table linking Group and Poll."""

    __tablename__ = 'grouppoll'

    grouppoll_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.poll_id'))
    group = db.relationship('Group', backref='polls')
    poll = db.relationship('Poll', backref='groups')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<GroupPoll id={self.grouppoll_id} group={self.group_id} poll={self.poll_id}>"


class Vote(ModelMixin, db.Model):
    """A response to a poll submitted by a user."""

    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.poll_id'))
    user = db.relationship('User', backref='votes')
    poll = db.relationship('Poll', backref='votes')
    response = db.Column(db.String(3), db.ForeignKey('responses.response_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Vote vote_id={self.vote_id}>"


class Response(ModelMixin, db.Model):
    """An expression of agreement or dissent used to respond to a poll."""

    __tablename__ = 'responses'

    response_id = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Response response_id={self.response_id}>"


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///consensy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    print("* Connected to DB.")


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
