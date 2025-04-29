import json
from unittest import mock

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


def test_command_connection_error(capsys):
    with mock.patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("No connection")
        with pytest.raises(APIException) as excinfo:
            call_command("download_revo_data")
        assert "API connection error" in str(excinfo.value)


def test_command_http_error(capsys):
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        with pytest.raises(APIException) as excinfo:
            call_command("download_revo_data")
        assert "HTTP error: Expected 200 OK, got 400" in str(excinfo.value)


def test_command_invalid_json(capsys):
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_get.return_value = mock_response

        with pytest.raises(ValueError) as exc:
            call_command("download_revo_data")
        assert "API response is not valid JSON." in str(exc.value)


def test_command_valid_response(capsys):
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "Test", "is_active": True, "tags": ["a", "b"]}
        ]
        mock_get.return_value = mock_response

        call_command("download_revo_data")
        captured = capsys.readouterr()
        assert "API data downloaded and parsed" in captured.out
        assert "ID: 1" in captured.out
