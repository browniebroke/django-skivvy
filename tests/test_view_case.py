import pytest
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.contrib.auth.models import User
from skivvy import ViewTestCase

from . import views


def test_get_url_params():
    class TheCase(ViewTestCase, TestCase):
        def setup_get_data(self):
            return {
                'some': 'abc def :/?#[]@!$&\'()*+,;=',
                'key': 'value'}

    case = TheCase()
    url_params = case._get_url_params()
    reserved_str = '%3A%2F%3F%23%5B%5D%40%21%24%26%27%28%29%2A%2B%2C%3B%3D'
    assert 'some=abc+def+%s' % reserved_str in url_params
    assert 'key=value' in url_params


def test_setup_models():
    class TheCase(ViewTestCase, TestCase):
        id = 0

        def setup_models(self):
            self.id = 1

    case = TheCase()
    assert case.id == 0
    case.setUp()
    assert case.id == 1


def test_setup_models_not_present():
    class TheCase(ViewTestCase, TestCase):
        id = 0

    case = TheCase()
    assert case.id == 0
    case.setUp()
    assert case.id == 0


def test_setup_view():
    class TheCase(ViewTestCase, TestCase):
        pass

    with pytest.raises(ImproperlyConfigured):
        case = TheCase()
        case.setup_view()


def test_setup_view_from_view_class():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericView

    case = TheCase()
    view = case.setup_view()
    assert view.__name__ == views.GenericView.__name__


def test_setup_view_from_view_class_with_view_kwargs():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericView

    case = TheCase()
    view = case.setup_view(view_kwargs={'test_arg': True})
    assert view.__name__ == views.GenericView.__name__
    assert view.view_initkwargs == {'test_arg': True}


def test_get_get_data_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_get_data(self):
            return {'some': 'data'}

    case = TheCase()
    get_data = case._get_get_data()
    assert get_data == {'some': 'data'}


def test_get_get_data_attribute():
    class TheCase(ViewTestCase, TestCase):
        get_data = {'some': 'data'}

    case = TheCase()
    get_data = case._get_get_data()
    assert get_data == {'some': 'data'}


def test_get_get_data_update():
    class TheCase(ViewTestCase, TestCase):
        get_data = {'some': 'data'}

    case = TheCase()
    get_data = case._get_get_data({'some': 'other'})
    assert get_data == {'some': 'other'}


def test_get_post_data_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_post_data(self):
            return {'some': 'data'}

    case = TheCase()
    post_data = case._get_post_data()
    assert post_data == {'some': 'data'}


def test_get_post_data_attribute():
    class TheCase(ViewTestCase, TestCase):
        post_data = {'some': 'data'}

    case = TheCase()
    post_data = case._get_post_data()
    assert post_data == {'some': 'data'}


def test_get_post_data_update():
    class TheCase(ViewTestCase, TestCase):
        post_data = {'some': 'data'}

    case = TheCase()
    post_data = case._get_post_data({'some': 'other'})
    assert post_data == {'some': 'other'}


def test_url_kwargs_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_url_kwargs(self):
            return {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_url_kwargs_attribute():
    class TheCase(ViewTestCase, TestCase):
        url_kwargs = {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_url_kwargs_update():
    class TheCase(ViewTestCase, TestCase):
        url_kwargs = {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_url_kwargs({'some': 'other'})
    assert url_kwargs == {'some': 'other'}


def test_get_template_context_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_template_context(self):
            return {'some': 'data'}

    case = TheCase()
    context = case._get_template_context()
    assert context == {'some': 'data'}


def test_get_template_context_attribute():
    class TheCase(ViewTestCase, TestCase):
        template_context = {'some': 'data'}

    case = TheCase()
    context = case._get_template_context()
    assert context == {'some': 'data'}


def test_get_template_context_unconfigured():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    context = case._get_template_context()
    assert context == {}


def test_get_template_unconfigured():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    with pytest.raises(ImproperlyConfigured):
        case._get_template()


def test_get_template_method():
    class TheCase(ViewTestCase, TestCase):
        template = 'some.html'

    case = TheCase()
    template = case._get_template()
    assert template == 'some.html'


def test_get_template_attribute():
    class TheCase(ViewTestCase, TestCase):
        def setup_template(self):
            return 'some.html'

    case = TheCase()
    template = case._get_template()
    assert template == 'some.html'


def _get_success_url_kwargs(self):
        if hasattr(self, 'setup_success_url_kwargs'):
            return self.setup_success_url_kwargs()
        elif hasattr(self, 'success_url_kwargs'):
            return self.success_url_kwargs
        else:
            return self._get_url_kwargs()


def test_get_success_url_kwargs_unconfigured():
    class TheCase(ViewTestCase, TestCase):
        def _get_url_kwargs(self):
            return {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_success_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_get_success_url_kwargs_attribute():
    class TheCase(ViewTestCase, TestCase):
        success_url_kwargs = {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_success_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_get_success_url_kwargs_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_success_url_kwargs(self):
            return {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_success_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_get_url_kwargs_unconfigured():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    url_kwargs = case._get_success_url_kwargs()
    assert url_kwargs == {}


def test_get_url_kwargs_attribute():
    class TheCase(ViewTestCase, TestCase):
        url_kwargs = {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_get_url_kwargs_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_url_kwargs(self):
            return {'some': 'data'}

    case = TheCase()
    url_kwargs = case._get_url_kwargs()
    assert url_kwargs == {'some': 'data'}


def test_get_success_url_unconfigured():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    with pytest.raises(ImproperlyConfigured):
        case.get_success_url()


def test_get_success_url_attribute():
    class TheCase(ViewTestCase, TestCase):
        success_url = '/success/'

    case = TheCase()
    url = case.get_success_url()
    assert url == '/success/'


def test_get_success_url_method():
    class TheCase(ViewTestCase, TestCase):
        success_url_name = 'success'
        success_url_kwargs = {'id': '1'}

    case = TheCase()
    url = case.get_success_url()
    assert url == '/success/1/'


def test_expected_success_url():
    class TheCase(ViewTestCase, TestCase):
        success_url_name = 'success'
        success_url_kwargs = {'id': '1'}

    case = TheCase()
    assert case.expected_success_url == '/success/1/'


def test_request_meta_attribute():
    class TheCase(ViewTestCase, TestCase):
        request_meta = {'HTTP_REFERER': 'http://example.com'}

    case = TheCase()
    request_meta = case._get_request_meta()
    assert request_meta == {'HTTP_REFERER': 'http://example.com'}


def test_request_meta_method():
    class TheCase(ViewTestCase, TestCase):
        def setup_request_meta(self):
            return {'HTTP_REFERER': 'http://example.com'}

    case = TheCase()
    request_meta = case._get_request_meta()
    assert request_meta == {'HTTP_REFERER': 'http://example.com'}


def test_request_meta_empty():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    request_meta = case._get_request_meta()
    assert request_meta == {}


def test_request_meta_overwrite():
    class TheCase(ViewTestCase, TestCase):
        pass

    case = TheCase()
    request_meta = case._get_request_meta(
        {'HTTP_REFERER': 'http://example.com'})
    assert request_meta == {'HTTP_REFERER': 'http://example.com'}


def test_render_content():
    class TheCase(ViewTestCase, TestCase):
        template = 'test.html'
        template_context = {'id': 'test-id'}
        _request = HttpRequest()

    case = TheCase()
    content = case.render_content()
    assert content == '<h1>test-id</h1>\n'


def test_render_content_update_context():
    class TheCase(ViewTestCase, TestCase):
        template = 'test.html'
        template_context = {'id': 'other-id'}
        _request = HttpRequest()

    case = TheCase()
    content = case.render_content(id='test-id')
    assert content == '<h1>test-id</h1>\n'


def test_expected_content():
    class TheCase(ViewTestCase, TestCase):
        template = 'test.html'
        template_context = {'id': 'test-id'}
        _request = HttpRequest()

    case = TheCase()
    content = case.expected_content
    assert content == '<h1>test-id</h1>\n'


def test_request_get():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericView
        request_meta = {'HTTP_REFERER': 'http://example.com'}

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'
    assert case._request.META['SERVER_NAME'] == 'testserver'
    assert case._request.META['SERVER_PORT'] == '80'
    assert case._request.META['HTTP_REFERER'] == 'http://example.com'

    assert response.status_code == 200
    assert response.content == '<h1>Test content<h1>'
    assert response.location is None
    assert 'content-type' in response.headers
    assert len(response.messages) == 1
    assert 'Hello world.' in response.messages


def test_request_overwrite():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericView
        request_meta = {'HTTP_REFERER': 'http://example.com'}

    case = TheCase()
    case.request(
        request_meta={'HTTP_REFERER': 'http://example.com/blah'})

    assert case._request.method == 'GET'
    assert case._request.META['SERVER_NAME'] == 'testserver'
    assert case._request.META['SERVER_PORT'] == '80'
    assert case._request.META['HTTP_REFERER'] == 'http://example.com/blah'


def test_request_get_template_response():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericTemplateView

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'

    assert response.status_code == 200
    assert response.content == '<h1>test-id</h1>\n'
    assert response.location is None
    assert 'content-type' in response.headers
    assert len(response.messages) == 0


def test_request_redirect_response():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericRedirectView

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user)

    assert case._request.user == user
    assert case._request.method == 'GET'

    assert response.status_code == 302
    assert response.content is ''
    assert response.location == '/redirect/'
    assert 'content-type' in response.headers
    assert len(response.messages) == 0


def test_request_post():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.GenericView
        post_data = {'data': 'abc def :/?#[]@!$&\'()*+,;='}

    user = User(username='user')
    case = TheCase()
    response = case.request(user=user, method='POST')

    assert case._request.user == user
    assert case._request.method == 'POST'

    assert response.status_code == 200
    assert response.content == '<h1>data: abc def :/?#[]@!$&\'()*+,;=<h1>'
    assert response.location is None
    assert 'content-type' in response.headers
    assert len(response.messages) == 0


def test_render_csrf_token():
    class TheCase(ViewTestCase, TestCase):
        view_class = views.CsrfTemplateView
        template = 'csrf.html'

    case = TheCase()
    response = case.request()

    assert response.status_code == 200
    assert response.content == case.expected_content
