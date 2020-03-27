# Consensy core server

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from jinja2 import StrictUndefined
from model import User, Group, Poll, Response, Vote, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""

    if 'current_user' in session:
        return redirect(f'/users/{session["current_user"]["user_id"]}')

    return render_template('homepage.html')


##############################################################################
# Routes for managing users


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


##############################################################################
# Routes for managing polls and votes


@app.route('/new_poll')
def display_new_poll():
    """Display form for creating a new poll."""

    return render_template('new_poll.html')


@app.route('/new_poll', methods=['POST'])
def create_new_poll():
    """Process info from new_poll.html form and add to database."""

    title = request.form.get('title')
    prompt = request.form.get('prompt')
    description = request.form.get('description')

    poll = Poll(title=title, prompt=prompt, description=description)
    db.session.add(poll)
    db.session.commit()

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
    """Display the results of a poll as a table."""

    poll = Poll.query.get(poll_id)

    results = poll.tally_results()

    return render_template('poll_results.html', poll=poll, result=results)


@app.route('/poll/results_chart')
def view_poll_results_chart(poll_id):
    """Display the results of a poll as a pie-chart."""

    poll = Poll.query.get(poll_id)

    results = poll.tally_results()

    return jsonify(results)


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
