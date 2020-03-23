# Consensy core server

from flask import Flask, render_template, redirect, request, flash, session
from jinja2 import StrictUndefined
from model import User, Group, Poll, Response, Vote, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


##############################################################################
# Routes for managing users


@app.route('/new_user', methods=['POST'])
def add_user():
    """Add a new user to user database with information provided. Send to user
       homepage via /login"""
    user_data = dict(request.form)
    QUERY = User.query.filter_by(email=user_data.get('email')).first()

    if QUERY is not None:
        flash('User already exists. Please log-in.')
        return redirect('/')
    else:
        # Add user to database.
        user = User(**user_data)
        user.save()

        # Update session dictionary.
        session['current_user'] = {'user_id': user.user_id}

        return redirect(f'/users/{user.user_id}')


@app.route('/login', methods=['POST'])
def login():
    """Validate email & password, update session, route to user homepage."""

    email = request.form.get('email')
    password = request.form.get('password')

    QUERY = User.query.filter_by(email=email).first()

    # Verify user exists.
    if QUERY is None:
        flash('User does not exist.')

    else:
        # Verify password.
        if QUERY.password == password:

            # Update session dictionary.
            session['current_user'] = {'user_id': QUERY.user_id}

            flash('Login successful.')
            return redirect(f'/users/{QUERY.user_id}')

        else:
            flash('Invalid password.')
            return redirect('/login_form')

    return redirect(f'/{QUERY.user_id}')


@app.route('/logout')
def logout():
    """Remove user data from session."""

    del session['current_user']

    return redirect('/')


@app.route('/users/<user_id>')
def display_user(user_id):
    """Display user landing page."""

    return render_template('user_page.html', user_id=user_id)


##############################################################################
# Routes for managing polls and votes


@app.route('/new_poll')
def display_new_poll():
    """Display form for creating a new poll."""

    return render_template('new_poll.html')


@app.route('/new_poll', methods=['POST'])
def create_new_poll():
    """Process info from new_poll.html form and add to database."""
    poll_data = dict(request.form)
    poll = Poll(**poll_data)
    poll.save()

    return redirect(f'poll/{poll.poll_id}')


@app.route('/poll/<poll_id>')
def display_poll(poll_id):
    """Display a poll."""

    poll = Poll.query.get(poll_id)

    return render_template('poll.html', poll=poll)


@app.route('/poll/<poll_id>/submit_vote', methods=['POST'])
def submit_vote(poll_id):
    """This view will process a vote."""

    response = request.form.get('response')
    user_id = session['current_user']['user_id']
    
    vote = Vote(user_id=user_id, response=response, poll_id=poll_id)
    db.session.add(vote)
    db.session.commit()

    return redirect(f'/poll/{poll_id}/results')


@app.route('/poll/<poll_id>/results')
def view_poll_results(poll_id):
    """Display the results of a poll."""

    poll = Poll.query.get(poll_id)

    results = poll.tally_results()

    return render_template('poll_results.html', poll=poll, result=results)


##############################################################################
# App configuration

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
