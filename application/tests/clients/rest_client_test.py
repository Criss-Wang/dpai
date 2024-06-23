from unittest.mock import MagicMock


def test_some_func(client_fixture):
    obj_mock = MagicMock()
    obj_mock.some_func.return_value = None
    assert True
