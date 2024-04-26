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

## UserViewSet API Endpoints