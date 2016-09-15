from django.test import TestCase
from django.contrib.auth.models import User
from skivvy import APITestCase

from .views import APITestView, APIXMLTestView, APIViewSetTestView


def test_request_get():
    class TheCase(APITestCase, TestCase):
        view_class = APITestView

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'

    assert response.status_code == 200
    assert isinstance(response.content, dict)
    assert response.content == {"some": "json"}
    assert response.location is None
    assert 'content-type' in response.headers
    assert response.headers['content-type'][1] == 'application/json'
    assert len(response.messages) == 0


def test_request_post():
    class TheCase(APITestCase, TestCase):
        view_class = APITestView
        post_data = {'some': 'json'}

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user, method='POST')

    assert case._request.user == user
    assert case._request.method == 'POST'

    assert response.status_code == 200
    assert isinstance(response.content, dict)
    assert response.content == {"some": "json"}
    assert response.location is None
    assert 'content-type' in response.headers
    assert response.headers['content-type'][1] == 'application/json'
    assert len(response.messages) == 0


def test_request_post_multipart():
    class TheCase(APITestCase, TestCase):
        view_class = APITestView
        post_data = {'some': 'json'}

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user,
                            method='POST',
                            content_type='multipart/form-data')

    assert case._request.user == user
    assert case._request.method == 'POST'

    assert response.status_code == 200
    assert isinstance(response.content, dict)
    assert response.content == {"some": ["json"]}
    assert response.location is None
    assert 'content-type' in response.headers
    assert response.headers['content-type'][1] == 'application/json'
    assert len(response.messages) == 0


def test_request_get_xml():
    class TheCase(APITestCase, TestCase):
        view_class = APIXMLTestView

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'

    assert response.status_code == 200
    assert isinstance(response.content, str)
    assert response.content == '<some>xml</some>'
    assert response.location is None
    assert 'content-type' in response.headers
    assert response.headers['content-type'][1] == 'application/xml'
    assert len(response.messages) == 0


def test_request_viewset_actions():
    class TheCase(APITestCase, TestCase):
        view_class = APIViewSetTestView
        viewset_actions = {'get': 'list'}

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'

    assert response.status_code == 200
    assert isinstance(response.content, dict)
    assert response.content == {"some": "json"}
    assert response.location is None
    assert 'content-type' in response.headers
    assert response.headers['content-type'][1] == 'application/json'
    assert len(response.messages) == 0
