from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from database import get_db
from models import SectionCreate, SectionUpdate, SectionResponse

router = APIRouter(tags=["Sections"])

@router.get("/exams/{exam_overview_id}/sections", response_model=List[SectionResponse])
def get_all_sections(exam_overview_id: int):
    """Get all sections for an exam"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM exam_overview WHERE exam_overview_id = %s", 
                       (exam_overview_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Exam not found")
            
            cur.execute("""
                SELECT s.section_id, s.exam_overview_id, s.section, 
                       s.no_of_questions, s.marks_per_question, s.total_marks, e.exam, e.grade, e.level
                FROM sections s INNER JOIN exam_overview e
                ON s.exam_overview_id = e.exam_overview_id
                WHERE s.exam_overview_id = %s
                ORDER BY section_id
            """, (exam_overview_id,))
            
            sections = cur.fetchall()
            return sections

@router.post("/exams/{exam_overview_id}/sections", response_model=SectionResponse, status_code=201)
def add_section(exam_overview_id: int, section: SectionCreate):
    """Add new section"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO sections 
                    (exam_overview_id, section, no_of_questions, 
                     marks_per_question, total_marks)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING section_id, exam_overview_id, section, 
                              no_of_questions, marks_per_question, total_marks
                """, (exam_overview_id, section.section, section.no_of_questions,
                      section.marks_per_question, section.total_marks))
                
                new_section = cur.fetchone()
                conn.commit()
                return new_section
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                # Check specific error types
                if "foreign key" in error_msg.lower():
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Exam not found with id {exam_overview_id}"
                    )
                elif "unique constraint" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Section already exists or duplicate: {error_msg}"
                    )
                elif "check constraint" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Validation failed: {error_msg}"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Database constraint violation: {error_msg}"
                    )
            except Exception as e:
                conn.rollback()
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Internal server error: {str(e)}"
                )

@router.put("/sections/{section_id}", response_model=SectionResponse)
def update_section(section_id: int, section: SectionUpdate):
    """Update section details"""
    with get_db() as conn:
        with conn.cursor() as cur:
            updates = []
            values = []
            
            if section.no_of_questions is not None:
                updates.append("no_of_questions = %s")
                values.append(section.no_of_questions)
            
            if section.total_marks is not None:
                updates.append("total_marks = %s")
                values.append(section.total_marks)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            values.append(section_id)
            
            cur.execute(f"""
                UPDATE sections
                SET {', '.join(updates)}
                WHERE section_id = %s
                RETURNING section_id, exam_overview_id, section, 
                          no_of_questions, marks_per_question, total_marks
            """, values)
            
            updated_section = cur.fetchone()
            
            if not updated_section:
                raise HTTPException(status_code=404, detail="Section not found")
            
            conn.commit()
            return updated_section

@router.delete("/sections/{section_id}", status_code=204)
def delete_section(section_id: int):
    """Delete section (cascade to syllabus)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM sections
                WHERE section_id = %s
            """, (section_id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Section not found")
            
            conn.commit()