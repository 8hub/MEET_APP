- [API documentation](#api-documentation)
- [MeetingViewSet API Endpoints](#meetingviewset-api-endpoints)
  - [`GET /meetings/`](#get-meetings)
  - [`GET /meetings/{id}/`](#get-meetingsid)
  - [`POST /meetings/`](#post-meetings)
  - [`PUT /meetings/{id}/`](#put-meetingsid)
  - [`DELETE /meetings/{id}/`](#delete-meetingsid)
  - [`POST /meetings/{id}/add_participant/`](#post-meetingsidadd_participant)
  - [`POST /meetings/{id}/remove_participant/`](#post-meetingsidremove_participant)
  - [`POST /meetings/{id}/clear_participants/`](#post-meetingsidclear_participants)
  - [`GET /meetings/{id}/get_participants/`](#get-meetingsidget_participants)
  - [`GET /meetings/{id}/get_participant_ids/`](#get-meetingsidget_participant_ids)
- [User API Endpoints](#user-api-endpoints)
  - [`POST /register/`](#post-register)
  - [`POST /login/`](#post-login)
  - [`POST /logout/`](#post-logout)
  - [`GET /user/`](#get-user)
## API documentation
The app is devided into 3 apps:
1. `MeetApp` - API  for sending and receiving info about meetings
2. `UserApp` - API for sending and receiving info about users
3. `SongApp` - API for sending and receiving info about song requests

## MeetingViewSet API Endpoints

### `GET /meetings/`
- Returns a list of all meetings.
- Response status: 200 OK

### `GET /meetings/{id}/`
- Returns the details of a specific meeting by its ID.
- Response status: 200 OK

### `POST /meetings/`
- Creates a new meeting.
- Response status: 201 Created

### `PUT /meetings/{id}/`
- Updates the details of a specific meeting by its ID.
- Response status: 200 OK

### `DELETE /meetings/{id}/`
- Deletes a specific meeting by its ID.
- Response status: 204 No Content

### `POST /meetings/{id}/add_participant/`
- Adds a participant to a specific meeting by its ID.
- Request body should include `user_id`.
- Response status: 201 Created if successful, 404 Not Found if user does not exist.

### `POST /meetings/{id}/remove_participant/`
- Removes a participant from a specific meeting by its ID.
- Request body should include `user_id`.
- Response status: 200 OK if successful, 404 Not Found if user does not exist.

### `POST /meetings/{id}/clear_participants/`
- Clears all participants from a specific meeting by its ID.
- Response status: 200 OK

### `GET /meetings/{id}/get_participants/`
- Returns a list of all participants in a specific meeting by its ID.
- Response status: 200 OK

### `GET /meetings/{id}/get_participant_ids/`
- Returns a list of all participant IDs in a specific meeting by its ID.
- Response status: 200 OK

## User API Endpoints

### `POST /register/`
- Registers a new user.
- Request body should include `username`, `email`, and `password`.
- Returns a `refresh` and `access` token upon successful registration.
- Response status: 201 Created if successful, 422 Unprocessable Entity if email or password is invalid, 400 Bad Request for other errors.

### `POST /login/`
- Logs in an existing user.
- Request body should include `username` and `password`.
- Returns a `refresh` and `access` token upon successful login.
- Response status: 200 OK if successful, 401 Unauthorized if credentials are invalid.

### `POST /logout/`
- Logs out an authenticated user.
- Request body should include the `refresh` token.
- Response status: 205 Reset Content if successful, 400 Bad Request if an error occurred.

### `GET /user/`
- Returns the details of the authenticated user.
- Response status: 200 OK