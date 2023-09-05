import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.users.models import User
from src.apps.users.views import UserDetailsView


@pytest.mark.django_db
def test_authentication_guard_when_not_authenticated():
    client = APIClient()
    url = reverse("user_details")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authentication_guard_when_authenticated(user: User):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user_details")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_details(user: User):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user_details")

    response = client.get(url)
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name


@pytest.mark.django_db
def test_update_user_details(user: User):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user_details")

    new_first_name = "UpdatedFirstName"
    new_last_name = "UpdatedLastName"
    request_data = {"first_name": new_first_name, "last_name": new_last_name}

    response = client.patch(url, request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == new_first_name
    assert response.data["last_name"] == new_last_name

    updated_user = User.objects.get(id=user.id)
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


@pytest.mark.django_db
def test_empty_queryset(user: User):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user_details")

    response = client.get(url)
    view = UserDetailsView()
    view.request = response.wsgi_request
    queryset = view.get_queryset()
    assert queryset.count() == 0
