import pytest


@pytest.fixture(scope="module")
def client_fixture():
    return "this is suppposed to be a fixture"
