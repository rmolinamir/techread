import pytest
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from pytest_factoryboy import register

from src.apps.users.models import User
from src.apps.users.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def user(db, user_factory: UserFactory) -> User:
    return user_factory.create()


@pytest.fixture
def superuser(db, user_factory: UserFactory) -> User:
    return user_factory.create(is_staff=True, is_superuser=True)


@pytest.fixture
def mock_request():
    factory = RequestFactory()
    request = factory.get("/")
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    auth_middleware = AuthenticationMiddleware(lambda req: None)
    auth_middleware.process_request(request)

    return request
