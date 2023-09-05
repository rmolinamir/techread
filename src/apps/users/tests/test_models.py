import pytest
from django.contrib.auth import get_user_model

from src.apps.users.models import User as UserModel

from .factories import UserFactory

User: UserModel = get_user_model()


@pytest.mark.django_db
def test_create_user(user: UserModel) -> None:
    # Attributes
    assert user._id is not None
    assert user.id is not None
    assert user.email is not None
    assert user.password is not None
    assert user.first_name is not None
    assert user.last_name is not None
    # Flags
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser(superuser: UserModel) -> None:
    # Attributes
    assert superuser._id is not None
    assert superuser.id is not None
    assert superuser.email is not None
    assert superuser.password is not None
    assert superuser.first_name is not None
    assert superuser.last_name is not None
    # Flags
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_get_full_name(user: UserModel) -> None:
    full_name = user.full_name
    assert full_name == f"{user.first_name} {user.last_name}"


@pytest.mark.django_db
def test_get_short_name(user: UserModel) -> None:
    short_name = user.short_name
    assert short_name == user.first_name


@pytest.mark.django_db
def test_update_user(user: UserModel) -> None:
    new_first_name = "NewFirstName"
    new_last_name = "NewLastName"
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.save()
    updated_user = User.objects.get(id=user.id)
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


@pytest.mark.django_db
def test_delete_user(user: UserModel) -> None:
    user_id = user.id
    user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=user_id)


@pytest.mark.django_db
def test_user_str(user: UserModel) -> None:
    assert str(user) == user.full_name


@pytest.mark.django_db
def test_user_normalized_email(user: UserModel) -> None:
    assert user.email == user.email.lower()


@pytest.mark.django_db
def test_superuser_normalized_email(superuser: UserModel) -> None:
    assert superuser.email == superuser.email.lower()


@pytest.mark.django_db
def test_create_user_with_invalid_email_raises(user_factory: UserFactory) -> None:
    with pytest.raises(ValueError):
        user_factory.create(email="invalid-email.com")


@pytest.mark.django_db
def test_create_user_without_firstname_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(first_name="")


@pytest.mark.django_db
def test_create_user_without_lastname_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(last_name="")


@pytest.mark.django_db
def test_create_user_without_email_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(email="")


@pytest.mark.django_db
def test_create_user_without_password_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(password="")


@pytest.mark.django_db
def test_create_superuser_without_is_superuser_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(is_superuser=False, is_staff=True)


@pytest.mark.django_db
def test_create_superuser_without_is_staff_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(is_superuser=True, is_staff=False)


@pytest.mark.django_db
def test_create_superuser_without_is_active_raises(user_factory: UserModel) -> None:
    with pytest.raises(ValueError):
        user_factory.create(is_superuser=True, is_staff=True, is_active=False)
