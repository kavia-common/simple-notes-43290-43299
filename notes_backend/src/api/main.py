from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import uuid4, UUID
from datetime import datetime

app = FastAPI(
    title="Simple Notes API",
    description="A FastAPI backend for managing notes with basic CRUD operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "notes", "description": "CRUD operations for notes"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, modify this to the domain(s) you wish to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the note")
    content: str = Field(..., min_length=1, description="Content/body of the note")

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated title of the note")
    content: Optional[str] = Field(None, min_length=1, description="Updated content/body of the note")

class Note(NoteBase):
    id: UUID = Field(..., description="Unique note identifier (UUID)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")


# In-memory notes storage
notes_db: Dict[UUID, Note] = {}


@app.get("/", tags=["health"])
def health_check():
    """Health Check Endpoint"""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get("/notes", response_model=List[Note], tags=["notes"], summary="Get all notes", description="Retrieve all notes in the system.")
def get_notes():
    """Retrieve all notes."""
    return list(notes_db.values())


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    tags=["notes"],
    summary="Create a new note",
    description="Create a new note by providing a title and content."
)
def create_note(note: NoteCreate):
    """Create a new note with a title and content."""
    new_id = uuid4()
    now = datetime.utcnow()
    new_note = Note(
        id=new_id,
        title=note.title,
        content=note.content,
        created_at=now,
        updated_at=now
    )
    notes_db[new_id] = new_note
    return new_note


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Retrieve a single note",
    description="Retrieve a note by its unique identifier."
)
def get_note(note_id: UUID):
    """Retrieve a note by ID."""
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    tags=["notes"],
    summary="Update a note",
    description="Update the title and/or content of an existing note."
)
def update_note(note_id: UUID, note_update: NoteUpdate):
    """Update an existing note (partial or full update)."""
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    updated_fields = note_update.dict(exclude_unset=True)
    updated_note = note.model_copy(update=updated_fields)
    updated_note.updated_at = datetime.utcnow()
    notes_db[note_id] = updated_note
    return updated_note


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["notes"],
    summary="Delete a note",
    description="Delete a note by its unique identifier."
)
def delete_note(note_id: UUID):
    """Delete a note by ID."""
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes_db[note_id]
    return

