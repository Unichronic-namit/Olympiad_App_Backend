from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from database import get_db
from models import ExamCreate, ExamUpdate, ExamResponse

router = APIRouter(prefix="/exams", tags=["Exam Overview"])

@router.get("", response_model=List[ExamResponse])
def get_all_exams():
    """Get all exams (filters optional)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT exam_overview_id, exam, grade, level, 
                       total_questions, total_marks, total_time_mins
                FROM exam_overview
                ORDER BY exam_overview_id
            """)
            exams = cur.fetchall()
            return exams

@router.get("/{exam_overview_id}", response_model=ExamResponse)
def get_exam_details(exam_overview_id: int):
    """Get details of a single exam"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT exam_overview_id, exam, grade, level, 
                       total_questions, total_marks, total_time_mins
                FROM exam_overview
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            exam = cur.fetchone()
            
            if not exam:
                raise HTTPException(status_code=404, detail="Exam not found")
            
            return exam

@router.post("", response_model=ExamResponse, status_code=201)
def create_exam(exam: ExamCreate):
    """Create a new exam"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO exam_overview 
                    (exam, grade, level, total_questions, total_marks, total_time_mins)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING exam_overview_id, exam, grade, level, 
                              total_questions, total_marks, total_time_mins
                """, (exam.exam, exam.grade, exam.level, exam.total_questions, 
                      exam.total_marks, exam.total_time_mins))
                
                new_exam = cur.fetchone()
                conn.commit()
                return new_exam
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                # Print the actual error for debugging
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Database constraint violation: {str(e)}"
                )

@router.put("/{exam_overview_id}", response_model=ExamResponse)
def update_exam(exam_overview_id: int, exam: ExamUpdate):
    """Update exam details"""
    with get_db() as conn:
        with conn.cursor() as cur:
            updates = []
            values = []
            
            if exam.total_marks is not None:
                updates.append("total_marks = %s")
                values.append(exam.total_marks)
            
            if exam.total_time_mins is not None:
                updates.append("total_time_mins = %s")
                values.append(exam.total_time_mins)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            values.append(exam_overview_id)
            
            cur.execute(f"""
                UPDATE exam_overview
                SET {', '.join(updates)}
                WHERE exam_overview_id = %s
                RETURNING exam_overview_id, exam, grade, level, 
                          total_questions, total_marks, total_time_mins
            """, values)
            
            updated_exam = cur.fetchone()
            
            if not updated_exam:
                raise HTTPException(status_code=404, detail="Exam not found")
            
            conn.commit()
            return updated_exam

@router.delete("/{exam_overview_id}", status_code=204)
def delete_exam(exam_overview_id: int):
    """Delete exam (cascade deletes all linked data)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM exam_overview
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Exam not found")
            
            conn.commit()
