import string
import random
from faker import Faker
from model import Response, db, connect_to_db
from server import app

fake = Faker()


def random_user():
    """Generate a random user."""

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.ascii_free_email()
    password = ''
    for i in range(15):
        password += random.choice(string.ascii_letters + string.digits)

    return(first_name, last_name, email, password)

    # Replace print statement with addition to SQL Database.


def random_group():
    """Generate a random group."""

    name = fake.company()

    return(name)


##############################################################################

def load_responses():
    """Load response data into database."""

    print("* Loading responses")

    for row in open("response.data"):
        row = row.rstrip()
        response_id, name, description = row.split('|')

        response = Response(response_id=response_id,
                            name=name,
                            description=description)

        db.session.add(response)
        db.session.commit()

    print("* Responses loaded")


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_responses()
