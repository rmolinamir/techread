import pytest

from src.apps.users.forms import UserCreationForm
from src.apps.users.models import User


@pytest.mark.django_db
def test_user_creation_form_with_valid_data():
    form_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "password1": "string123456",
        "password2": "string123456",
    }
    form = UserCreationForm(data=form_data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_user_creation_form_with_invalid_data(user: User):
    form_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": user.email,
        "password1": "string123456",
        "password2": "string123456",
    }
    form = UserCreationForm(data=form_data)
    assert form.is_valid() is False
    assert "email" in form.errors
