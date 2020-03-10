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


@app.route('/new_user', methods=['POST'])
def add_user():
    """Add a new user to user database with information provided. Send to user
       homepage via /login"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    QUERY = User.query.filter_by(email=email).first()

    if QUERY is not None:
        flash('User already exists. Please log-in.')
        return redirect('/')

    else:
        # Add user to database.
        user = User(fname=first_name, lname=last_name, email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()

        # Update session dictionary.
        session['current_user'] = {'user_id': user.user_id,
                                   'email': user.email,
                                   'password': user.password,
                                   'first_name': user.fname,
                                   'last_name': user.lname}

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
            session['current_user'] = {'user_id': QUERY.user_id,
                                       'email': QUERY.email,
                                       'password': QUERY.password,
                                       'first_name': QUERY.fname,
                                       'last_name': QUERY.lname}

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


@app.route('/polls/<poll_id>')
def display_poll(poll_id):
    """Display a poll."""

    poll_id = 1

    return render_template('poll.html', poll_id=poll_id)


@app.route('/submit_vote')
def submit_vote():
    """This view will process a vote."""

    pass


@app.route('/display_results')
def display_results():
    """This view will process poll results."""

    pass


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
