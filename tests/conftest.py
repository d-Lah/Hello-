
import pytest
import random
import datetime
from first_app.db import db
from first_app.models import (User,
                              Post,
                              Comment,
                              FileUpload)
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
    last_digits = str(random.random())[-9:]
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
def create_post(app,send_data_for_post_api, new_user):
    data = send_data_for_post_api
    
    author_id = new_user.id
    author_name = new_user.first_name
    title = data["title"]
    body = data["body"]
    file_id = data["file_id"]
    current_datetime = datetime.datetime.today()
    post = Post(
        author_id = author_id,
        user_name = author_name,
        title = title,
        body = body,
        file_id = file_id,
        created = current_datetime 
    )
    db.session.add(post)
    db.session.commit()
    db.session.flush()
    return post

@pytest.fixture()
def create_comment(
    new_user,
    create_post,
    send_data_for_comment_api):

    data = send_data_for_comment_api
    author_id = new_user.id
    _post = create_post
    author_name = new_user.first_name
    text = data["text"]
    current_datetime = datetime.datetime.today()

    comment = Comment(
        author_id=author_id,
        post_id=_post.id,
        user_name=author_name,
        created=current_datetime,
        text=text)
    
    db.session.add(comment)
    db.session.commit()
    db.session.flush()
    return comment

@pytest.fixture()
def user_headers(new_user):
    _access_token = login_user(new_user)
    return {
        "Authorization": f"Bearer {_access_token}"
    }

@pytest.fixture()
def create_file(app):
    file_url = "test.jpg"
    file = FileUpload(url = file_url)
    db.session.add(file)
    db.session.commit()
    db.session.flush()
    return file.id

@pytest.fixture()
def send_data_for_post_api(app, create_file):
    title = "test"
    body = "test"
    file_id = create_file
    
    return {"title":title,
            "body":body,
            "file_id":file_id}

@pytest.fixture()
def send_data_for_comment_api(app):
    text = "test"
    return {"text": text}

@pytest.fixture()
def send_data_for_user_api(app):
    last_digits = str(random.random())[-9:]
    phone_number = f"7414750831{last_digits}"
    first_name = f"user{last_digits}" 
    second_name = f"User{last_digits}"
    password = "password"
    return {
        "phone_number" : phone_number,
        "first_name" : first_name,
        "second_name" : second_name,
        "password" : password
        }

@pytest.fixture()
def send_data_for_change_password(app):
    old_password = "password"
    new_password = "password"
    return{
        "old_password": old_password,
        "new_password": new_password
    }

@pytest.fixture()
def send_data_with_exists_phone_number_for_use_api(
        app,
        new_user):
    
    phone_number = new_user.phone_number
    last_digits = str(random.random())[-9:]
    first_name = f"user{last_digits}" 
    second_name = f"User{last_digits}"
    password = "password"
    
    return {
        "phone_number" : phone_number,
        "first_name" : first_name,
        "second_name" : second_name,
        "password" : password
        }

@pytest.fixture()
def send_data_with_wrong_old_password_for_change_password(app):
    old_password = "password0"
    new_password = "password"
    return{
        "old_password": old_password,
        "new_password": new_password
    }