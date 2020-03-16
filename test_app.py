import os
import pytest

from io import BytesIO

from app import process_line, get_numbers_from_file, UPLOAD_FOLDER
from app import app


def test_process_line():
    """
    can we handle different possible line content?
    """
    r = process_line('Alabama	Bay Minette 	8342')
    assert r == [8342]
    r = process_line('1 2 3')
    assert r == [1, 2, 3]
    r = process_line('aaa bbb ccc 1 2 zzz ! ><?c 444')
    assert r == [1, 2, 444]
    r = process_line('')
    assert r == []


def test_get_numbers_from_file(fs):
    """
    can we read from a file and get a list of numbers?
    """
    filename = 'test.txt'
    fs.create_file(os.path.join(UPLOAD_FOLDER, filename))
    with open(os.path.join(UPLOAD_FOLDER, filename), 'w') as f:
        f.write('1 2 3 4\n')
        f.write('Alabama	Bay Minette 	8342\n')
    r = get_numbers_from_file(filename)
    assert r == {'numbers': [1, 2, 3, 4, 8342], 'count': 5}


@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_index_page(test_client):
    """
    can we get the page?
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_post_index_page(test_client, fs):
    """
    can we post a file to the page?
    """
    filename = 'test.txt'
    data = {
        'file': (BytesIO(b'1 2 3 4'), filename),
    }
    fs.create_dir(UPLOAD_FOLDER)
    response = test_client.post('/', data=data)
    assert response.status_code == 200
    assert os.path.exists(os.path.join(UPLOAD_FOLDER, filename))
