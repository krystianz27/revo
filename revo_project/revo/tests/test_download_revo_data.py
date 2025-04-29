import json

import pytest
import requests
from django.core.management import call_command
from revo.management.commands.download_revo_data import APIException, validate_data


@pytest.mark.parametrize(
    "invalid_data, expected_error",
    [
        ({"not": "a list"}, "Received data is not a list."),
        ([{"id": 1}], "Missing required keys in dictionary."),
        (
            [{"id": "1", "name": "a", "is_active": True, "tags": []}],
            "Field 'id' is not an integer.",
        ),
        (
            [{"id": 1, "name": 123, "is_active": True, "tags": []}],
            "Field 'name' is not a string.",
        ),
        (
            [{"id": 1, "name": "a", "is_active": "yes", "tags": []}],
            "Field 'is_active' is not a boolean.",
        ),
        (
            [{"id": 1, "name": "a", "is_active": True, "tags": [1]}],
            "Field 'tags' is not a list of strings.",
        ),
    ],
)
def test_validate_data_invalid(invalid_data, expected_error):
    with pytest.raises(ValueError) as exc:
        validate_data(invalid_data)
    assert expected_error in str(exc.value)


def test_command_connection_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("No connection")

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(APIException) as exc:
        call_command("download_revo_data")
    assert "API connection error" in str(exc.value)


def test_command_http_error(monkeypatch):
    class MockResponse:
        status_code = 400

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    with pytest.raises(APIException) as exc:
        call_command("download_revo_data")
    assert "HTTP error: Expected 200 OK, got 400" in str(exc.value)


def test_command_invalid_json(monkeypatch):
    class MockResponse:
        status_code = 200

        def json(self):
            raise json.JSONDecodeError("Expecting value", "", 0)

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    with pytest.raises(ValueError) as exc:
        call_command("download_revo_data")
    assert "API response is not valid JSON." in str(exc.value)


def test_command_valid_response(monkeypatch, capsys):
    class MockResponse:
        status_code = 200

        def json(self):
            return [{"id": 1, "name": "Test", "is_active": True, "tags": ["a", "b"]}]

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    call_command("download_revo_data")
    captured = capsys.readouterr()
    assert "API data downloaded and parsed" in captured.out
    assert "ID: 1" in captured.out
