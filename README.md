# simple-notes-43290-43299

## Notes Backend API

A FastAPI backend for managing notes.

### Endpoints

#### Health Check

`GET /`

- Returns API health.

#### Get All Notes

`GET /notes`

- Response: 200 OK
- Returns a list of all notes.

**Example:**
```sh
curl -X GET http://localhost:3001/notes
```

#### Create Note

`POST /notes`

- Request body: JSON
    - `title` (str, required)
    - `content` (str, required)

- Response: 201 Created

**Example:**
```sh
curl -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Note", "content": "This is my note"}'
```

#### Get Note by ID

`GET /notes/{id}`

- Path parameter: `id` (UUID)
- Response: 200 OK

**Example:**
```sh
curl -X GET http://localhost:3001/notes/<note_id>
```

#### Update Note

`PUT /notes/{id}`

- Path parameter: `id` (UUID)
- Request body: JSON (any of the fields)
    - `title` (str, optional)
    - `content` (str, optional)
- Response: 200 OK

**Example:**
```sh
curl -X PUT http://localhost:3001/notes/<note_id> \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title"}'
```

#### Delete Note

`DELETE /notes/{id}`

- Path parameter: `id` (UUID)
- Response: 204 No Content

**Example:**
```sh
curl -X DELETE http://localhost:3001/notes/<note_id>
```

---

*All endpoints return appropriate error codes for validation or missing resources.*

- Full API docs at `/docs` (Swagger UI) when running.
