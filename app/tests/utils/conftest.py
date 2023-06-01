import pytest
from random import randint, random
from django.test import Client
from app.tests.users.factories import UserFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def random_email():
    return "email{}@email.com".format(random())


@pytest.fixture
def random_username():
    return "username{}".format(random())


@pytest.fixture
def random_id(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


@pytest.fixture
def user():
    return UserFactory()
