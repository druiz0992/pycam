import pytest
from pycam.errors import handle_errors, CommandError, AuthenticationError
from pycam.api.tapo import PytapoClient
from types import SimpleNamespace


def test_handle_errors_raises_command_error():
    @handle_errors()
    def faulty_function():
        raise ValueError("Something went wrong")

    with pytest.raises(CommandError) as exc_info:
        faulty_function()

    assert "Something went wrong" in str(exc_info.value)


def test_handle_errors_preserves_message():
    @handle_errors()
    def test_func():
        raise RuntimeError("boom")

    with pytest.raises(CommandError) as exc_info:
        test_func()

    assert "boom" in str(exc_info.value)
    assert isinstance(exc_info.value, CommandError)


def test_handle_errors_custom_type():
    class CustomError(Exception):
        pass

    @handle_errors(error_type=CustomError)
    def func():
        raise ValueError("bad stuff")

    with pytest.raises(CustomError) as exc_info:
        func()

    assert "bad stuff" in str(exc_info.value)


class FakeTapo:
    def __init__(self, host, user, password):
        raise AuthenticationError("Invalid credentials")


def test_handle_errors_on_init(monkeypatch):
    monkeypatch.setattr("pycam.api.tapo.Tapo", FakeTapo)
    config = SimpleNamespace(
        host="123", user_cloud="hello", password_cloud="really fake"
    )

    with pytest.raises(AuthenticationError) as exc_info:
        PytapoClient(config)

    assert "Invalid credentials" in str(exc_info.value)
