# CV Builder

CV Builder is a web application that allows users to create and manage their professional CVs (resumes) easily.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Testing](#testing)
## Project Description

CV Builder simplifies the process of creating personalized CVs. Users can create an account, enter their details, and customize the content of their CVs.

The project is built using the Django web framework and Django-Ninja for creating the API endpoints.

## Installation

To run the CV Builder locally, follow these steps:

1. Clone the repository: `git clone https://github.com/Farida-98-cse/CvBuilder.git`
2. Change into the project directory: `cd CvBuilder`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Run the migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`

## API Documentation

The CV Builder project exposes a set of API endpoints using Django-Ninja.
For detailed API documentation, please refer to the [API Documentation](http://127.0.0.1:8000/api/docs).

The API documentation includes information on the available endpoints, request formats, response formats, and authentication requirements. It also provides example requests and responses for each endpoint.


## Testing

CV Builder includes a comprehensive test suite using pytest. To run the tests, follow these steps:

1. Activate the virtual environment (if not already activated).
2. Run pytest: `pytest`

The test suite ensures that the application functions correctly and helps maintain code quality.