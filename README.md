# Revo Project

This is a Django project for downloading data from an external API, parsing it,
and handling errors. It includes a management command `download_revo_data` which
fetches data from an API, handles possible errors, and validates the structure
of the data.

## Features

- A custom management command `download_revo_data` that:
  - Sends an HTTP GET request to a non-existent URL.
  - Attempts to parse the response as JSON.
  - Handles connection errors, HTTP errors, and invalid data formats.
  - Prints parsed data in a readable format to the console.

## Basic View of Project Structure

    revo/
    ├── venv/
    ├── revo_project/
    │   ├── revo_project/
    │   ├── revo/
    │   └── manage.py
    ├── requirements.txt

## Requirements

- Python 3.13
- `Django` 5.2
- `requests` library for HTTP requests
- `pytest` for testing

## Installation

1. Clone the repository: `git clone repository-url`

2. Navigate to the project folder: `cd revo`

3. Create a virtual environment: `python -m venv venv`

4. Activate the virtual environment:

    - On Windows:

          .\venv\Scripts\activate

    - On macOS/Linux:

          source venv/bin/activate

5. Install required dependencies:

        pip install -r requirements.txt

6. Navigate to the Django project folder `revo_project`:

        cd revo_project

## Running the Command

This will attempt to fetch data from a non-existent API and print the result or
errors. Run from `revo_project/`

    python manage.py download_revo_data

## Running Tests

To run tests with `pytest` Run from `revo_project/`:

    pytest

This will run all the tests and check that the command behaves correctly under
various scenarios.

## Testing Scenarios

The tests cover the following scenarios:

1. **Connection Error**: Simulates a connection error when trying to fetch data
   from the API.
2. **HTTP Error**: Simulates an HTTP error (non-200 status code) while fetching
   data.
3. **Invalid Data**: Simulates invalid data from the API and checks that the
   command handles errors correctly.
4. **Valid Data**: Simulates valid data and checks that the command correctly
   processes and prints the data.
