from fastapi import APIRouter, HTTPException
import psycopg2
from database import get_db
from models import ExamResponse, UserExamRequest, UserExamResponse
from typing import List

router = APIRouter(tags=["User Exams"])

@router.get("/user_exam/{user_id}", response_model=List[ExamResponse])
def get_user_exams(user_id: int):
    """Get all exams for a specific user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Join user_exams with exam_overview to get exam details
                cur.execute("""
                    SELECT 
                        eo.exam_overview_id,
                        eo.exam,
                        eo.grade,
                        eo.level,
                        eo.total_questions,
                        eo.total_marks,
                        eo.total_time_mins
                    FROM user_exams ue
                    INNER JOIN exam_overview eo
                        ON ue.exam_overview_id = eo.exam_overview_id
                    WHERE ue.user_id = %s
                    ORDER BY eo.grade, eo.level
                """, (user_id,))
                
                exams = cur.fetchall()
                
                # If no exams found for the user
                if not exams:
                    return []
                
                # Convert to list of dictionaries
                exam_list = []
                for exam in exams:
                    exam_list.append({
                        "exam_overview_id": exam['exam_overview_id'],
                        "exam": exam['exam'],
                        "grade": exam['grade'],
                        "level": exam['level'],
                        "total_questions": exam['total_questions'],
                        "total_marks": exam['total_marks'],
                        "total_time_mins": exam['total_time_mins']
                    })
                
                return exam_list
                
            except psycopg2.Error as e:
                print(f"Database Error: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to fetch user exams")

@router.post("/user_exam/{user_id}", response_model=List[UserExamResponse], status_code=201)
def add_user_exams(user_id: int, request: UserExamRequest):
    """Add exams for a specific user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # First check if user exists
                cur.execute("""
                    SELECT user_id FROM users 
                    WHERE user_id = %s AND is_active = TRUE
                """, (user_id,))
                
                if not cur.fetchone():
                    raise HTTPException(
                        status_code=404, 
                        detail="User not found or inactive"
                    )
                
                # Check if exam_overview_ids exist
                if not request.exam_overview_ids:
                    raise HTTPException(
                        status_code=400,
                        detail="At least one exam_overview_id is required"
                    )
                
                # Prepare data for batch insert
                exam_data = [(user_id, exam_id) for exam_id in request.exam_overview_ids]
                
                # Insert exams and return created records
                created_exams = []
                for user_id_val, exam_id in exam_data:
                    cur.execute("""
                        INSERT INTO user_exams 
                        (user_id, exam_overview_id)
                        VALUES (%s, %s)
                        RETURNING user_exam_id, user_id, exam_overview_id, 
                                  start_date, end_date, status
                    """, (user_id_val, exam_id))
                    
                    created_exam = cur.fetchone()
                    created_exams.append(created_exam)
                
                conn.commit()
                print(f"Added {len(created_exams)} exams for user {user_id}")
                
                return created_exams
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail="Invalid exam_overview_id provided"
                    )
                elif "duplicate key" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail="Exam already exists for this user"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Failed to add exams: {error_msg}"
                    )
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to add user exams"
                )