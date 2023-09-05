import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from src.apps.users.models import User as UserModel
from src.apps.users.serializers import CustomRegisterSerializer, UserSerializer

User: UserModel = get_user_model()


@pytest.mark.django_db
def test_user_serializer(user: UserModel) -> None:
    serializer = UserSerializer(user)
    assert "id" in serializer.data
    assert "email" in serializer.data
    assert "password" not in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "gender" in serializer.data
    assert "phone_number" in serializer.data
    assert "profile_photo" in serializer.data
    assert "country" in serializer.data
    assert "city" in serializer.data


@pytest.mark.django_db
def test_user_to_representation(user: UserModel) -> None:
    serializer = UserSerializer(user)
    assert "admin" not in serializer.data


@pytest.mark.django_db
def test_superuser_to_representation(superuser: UserModel) -> None:
    serializer = UserSerializer(superuser)
    assert "admin" in serializer.data
    assert serializer.data["admin"] is True


@pytest.mark.django_db
def test_custom_register_serializer_with_valid_data(mock_request) -> None:
    register_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "password1": "string123456",
        "password2": "string123456",
    }
    serializer = CustomRegisterSerializer(data=register_data)
    assert serializer.is_valid() is True

    user: UserModel = serializer.save(mock_request)
    assert user.first_name == register_data["first_name"]
    assert user.last_name == register_data["last_name"]
    assert user.email == register_data["email"]


@pytest.mark.django_db
def test_custom_register_serializer_with_invalid_data() -> None:
    register_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "email@example.com",
        "password1": "foo123456",
        "password2": "bar123456",
    }
    serializer = CustomRegisterSerializer(data=register_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
