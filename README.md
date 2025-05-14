## How to run

`cp .env.example .env` and set in .env your SECRET_KEY value  
`docker-compose up --build`  
`docker-compose exec web python manage.py migrate`  

Now you can access the API at http://localhost:8000/.

## API DOCS

### Authentication

The API uses Basic Authentication for most endpoints. Make sure to include the appropriate Authorization header for authenticated endpoints.

### Register a New User (No Authentication Required)

**Endpoint:** /api/accounts/register/

**Method:** POST

**Permissions:** Public (No authentication required)

**Request Body:**

{
    "username": "newuser",
    "password": "password",
    "email": "newuser@example.com"
}

**Response:**

201 Created – User registered successfully

400 Bad Request – Validation error

**Example Response:**

{
    "message": "User registered successfully"
}

### Event List and Creation

**Endpoint:** /api/events/

**Methods:**

GET – List all events

POST – Create a new event (authenticated)

**Permissions:**

GET – Public (No authentication required)

POST – Authenticated users (Organizer is set automatically - it is the authenticated user)

**Request Body (POST):**

{
    "title": "My First Event",
    "description": "This is a description of my first event.",
    "date": "2025-05-15T18:30:00Z",
    "location": "New York"
}

**Response:**

201 Created – Event created successfully

400 Bad Request – Validation error

### Retrieve, Update, and Delete Event

**Endpoint:** /api/events/{id}/

**Methods:**

GET – Retrieve event details (No authentication required)

PUT – Update event (only the organizer)

PATCH – Partially update event (only the organizer)

DELETE – Delete event (only the organizer)

**Permissions:** Organizer only for PUT, PATCH, DELETE

**Response:**

200 OK – Event details

403 Forbidden – Not the organizer

404 Not Found – Event not found

### Invite Users to Event

**Endpoint:** /api/events/{id}/invite/

**Method:** POST

**Note:** Only the event organizer can invite users.

**Permissions:** Organizer only

**Request Body:**

{
    "invited_user_ids": [2, 3, 5]
}

**Response:**

200 OK – Users invited successfully

400 Bad Request – Invalid data

403 Forbidden – Not the organizer

**Example Response:**

{
    "invited": ["user2"],
    "already_invited": ["user3"],
    "already_registered": ["user5"],
    "not_found": [99]
}

### Confirm Registration

**Endpoint:** /api/events/{id}/confirm_registration/

**Method:** POST

**Note:** Users must be invited before they can confirm their registration.

**Permissions:** Authenticated users (the authenticated user is the one to be registered)

**Request Body:**

EMPTY

**Response:**

200 OK – User successfully registered for the event

400 Bad Request – User already registered

403 Forbidden – User not invited to this event

**Example Response:**

{
    "message": "user123 registered for the event"
}

### Filtering, Searching, and Ordering

**Filtering:**

Filter by title: /api/events/?title=conference

Filter by location: /api/events/?location=New York

Filter by organizer: /api/events/?organizer=johndoe

Filter by date range: /api/events/?date_after=2025-05-01&date_before=2025-05-31

**Searching:**

Search by title, description, location, or organizer: /api/events/?search=workshop

**Ordering:**

Order by date: /api/events/?ordering=date

Reverse order by date: /api/events/?ordering=-date

### Notes

Invited Users: Users must be invited before they can confirm their registration.

Organizer Permissions: Only the event organizer can invite users and modify the event.

Basic Authentication: Required for all endpoints except registration and getting the events.

