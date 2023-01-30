
# Social API

A Flask API that allows users to register, get, delete, and change password of their account.

## Requirements

-   Flask
-   Flask-RESTx

## Usage

To run the API:

rubyCopy code

`$ python app.py` 

## Endpoints

### POST `/user`

-   Registers a user by taking in:
    -   `username` (str, required)
    -   `year of birth` (int, required)
    -   `month of birth` (int, required)
    -   `day of birth` (int, required)
    -   `password` (str, required)
    -   `email` (str, required)
    -   `gender` (str, optional)
-   Age restriction: user must be 18+ years old.

### GET `/user/<id>`

-   Returns the details of the user account with the given `id`.

### DELETE `/user/<id>`

-   Deletes the user account with the given `id`.

### PUT `/user/change_password`

-   Changes password of the user account with the given `id` by taking in:
    -   `id` (str, required)
    -   `new password` (str, required)
    -   `repeat new password` (str, required)
-   Both new passwords must match.

# JsonEncoder

This file contains a custom JSON encoder class `JsonEncoder` that extends `JSONEncoder` from the `json` module. This class is used to handle encoding of date objects in a specific way, allowing them to be serialized to JSON forma