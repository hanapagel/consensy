import string
import random
from faker import Faker

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
