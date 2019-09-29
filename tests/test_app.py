import json
import pytest

from app import api


@pytest.fixture
def client():
    client = api.test_client()
    return client


def test_get_not_allowed(client):
    # method not supported
    response = client.get('/nearest')
    assert response.status_code == 405


@pytest.mark.usefixtures("client")
def test_post_no_data(client):
    # no data was sent
    response = client.post('/nearest', json={}, content_type='application/json')
    assert response.status_code == 400


@pytest.mark.usefixtures("client")
def test_post_file_color_not_found(client):
    # random all-red image that will not match any of the testers
    data = {
        'image': 'https://colourlex.com/wp-content/uploads/2015/08/Cadmium_red_nr_2_painted_swatch_Lipscher-225-opt.jpg'
    }

    response = client.post('/nearest', json=data, content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'application/json'

    color = json.loads(response.get_data())['color']

    assert color == 'No color found'


@pytest.mark.usefixtures("client")
def test_post_file_color_found(client):
    # valid image, download and find color (warning: slow)
    data = {
        'image': 'https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-navy.png'
    }
    
    response = client.post('/nearest', json=data, content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'application/json'

    color = json.loads(response.get_data())['color']

    assert color == 'navy'