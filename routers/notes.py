from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from database import get_db
from models import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(tags=["Notes"])

@router.get("/exams/{exam_overview_id}/notes", response_model=List[NoteResponse])
def get_all_notes(exam_overview_id: int):
    """Get all notes for an exam"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Check if exam exists
            cur.execute("SELECT 1 FROM exam_overview WHERE exam_overview_id = %s", 
                       (exam_overview_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Exam not found")
            
            cur.execute("""
                SELECT note_id, note, exam_overview_id
                FROM notes
                WHERE exam_overview_id = %s
                ORDER BY note_id
            """, (exam_overview_id,))
            
            notes = cur.fetchall()
            return notes

@router.post("/exams/{exam_overview_id}/notes", response_model=NoteResponse, status_code=201)
def add_note(exam_overview_id: int, note: NoteCreate):
    """Add new note"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO notes (note, exam_overview_id)
                    VALUES (%s, %s)
                    RETURNING note_id, note, exam_overview_id
                """, (note.note, exam_overview_id))
                
                new_note = cur.fetchone()
                conn.commit()
                return new_note
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(status_code=404, detail="Exam not found")
                else:
                    raise HTTPException(status_code=400, detail=f"Database constraint violation: {error_msg}")

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate):
    """Update note"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE notes
                SET note = %s
                WHERE note_id = %s
                RETURNING note_id, note, exam_overview_id
            """, (note.note, note_id))
            
            updated_note = cur.fetchone()
            
            if not updated_note:
                raise HTTPException(status_code=404, detail="Note not found")
            
            conn.commit()
            return updated_note

@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    """Delete note"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM notes
                WHERE note_id = %s
            """, (note_id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Note not found")
            
            conn.commit()