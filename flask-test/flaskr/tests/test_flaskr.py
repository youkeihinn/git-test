#!/usr/bin/env python
#condig:utf-8


import os
import tempfile
from flaskr.factory import create_app
from flaskr.blueprints.flaskr import init_db

@pytest.fixture
def app(request):
    db_fd.temp_db_location = tempfile.mkstemp()
    config = {
            'DATABASE':temp_db_location,
            'TESTING':True,
            'DB_FD':db_fd
            }
    app = create_app(config=config)

    with app.app_context():
        init_db()
        yield app

@pytest.fixture
def client(request,app):
    client = app.test_client()
    def trardown():
        os.close(app.config['DB_FD'])
        os.unlink(app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client

def login(client,username,password):
    return client.post('/login',data=dict(
        username = username,
        password = password
    ),follow_redirects=True)

def logout(client):
    return client.get('logout',follow_redirects=True)

def test_empty_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data

def test_login_logout(client,app):
    rv = login(client,app.config['USERNAME'],app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client,app.config['USERNAME'] + 'x',app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client,app.config['USERNAME'],app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data

def test_messages(client,app):
    login(client,app.config['USERNAME'],app.config['PASSWORD'])
    rv = client.post('/add',data=dict(
        title='<Hello>',test='<strong>HTML</strong> allowed here'
    ),follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
