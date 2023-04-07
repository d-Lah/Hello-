
import pytest
import random
from first_app.db import db
from first_app.models import User
from first_app.app import create_app
from first_app.api.user import login_user
from werkzeug.security import check_password_hash, generate_password_hash

@pytest.fixture(autouse=True)
def app():
    app = create_app()
    app.app_context().push()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def new_user(app):
    last_digits = str(random.random())[-3:]
    phone_number = f"0685087{last_digits}"
    first_name = f"Andy{last_digits}"
    second_name = f"Kovv{last_digits}"
    password = "password"
    new_user = User(
        phone_number,
        first_name,
        second_name,
        generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()
    db.session.flush()
    return new_user

@pytest.fixture()
def user_headers(new_user):
    _access_token = login_user(new_user)
    return {
        "Authorization": f"Bearer {_access_token}"
    }