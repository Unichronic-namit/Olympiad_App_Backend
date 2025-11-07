from fastapi import APIRouter, HTTPException
import psycopg2
import json
from database import get_db
from models import UserPracticeExamRequest, UserPracticeExamResponse

router = APIRouter(tags=["User Practice Exams"])

@router.post("/user_practice_exam", response_model=UserPracticeExamResponse, status_code=201)
def add_user_practice_exams(request: UserPracticeExamRequest):
    """Add practice exam for a specific user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Validate input
                if not request.exam_overview_id and not request.user_id and not request.section_id and not request.syllabus_id and request.difficulty is None:
                    raise HTTPException(
                        status_code=400,
                        detail="All fields are required: user_id, exam_overview_id, section_id, syllabus_id, difficulty"
                    )
                
                # Insert into user_practice_exam table
                cur.execute("""
                    INSERT INTO user_practice_exam
                    (user_id, exam_overview_id, section_id, syllabus_id, difficulty)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (request.user_id, request.exam_overview_id, request.section_id, request.syllabus_id, request.difficulty))
                
                # Fetch the inserted row from user_practice_exam
                user_practice_exam_data = cur.fetchone()
                
                # Extract the user_practice_exam_id and created_at
                user_practice_exam_id = user_practice_exam_data['user_practice_exam_id']
                created_at = user_practice_exam_data['created_at']
                
                print(f"Created practice exam with ID: {user_practice_exam_id}")
                
                # Insert into practice_exam_attempt_details table
                cur.execute("""
                    INSERT INTO practice_exam_attempt_details
                    (user_practice_exam_id, que_ans_details, score, total_time, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (user_practice_exam_id, json.dumps([]), 0, 0, created_at, None))
                
                # Fetch the inserted row from practice_exam_attempt_details
                attempt_details_data = cur.fetchone()
                
                # Extract practice_exam_attempt_details_id
                practice_exam_attempt_details_id = attempt_details_data['practice_exam_attempt_details_id']
                
                print(f"Created attempt details with ID: {practice_exam_attempt_details_id}")
                print(f"User practice exam data: {user_practice_exam_data}")
                print(f"Attempt details data: {attempt_details_data}")
                
                conn.commit()
                
                # Combine data from both tables
                combined_response = {
                    **user_practice_exam_data,  # Spread all fields from first table
                    'practice_exam_attempt_details_id': practice_exam_attempt_details_id  # Add field from second table
                }
                
                return combined_response
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail="Invalid foreign key reference (user_id, exam_overview_id, section_id, or syllabus_id)"
                    )
                elif "duplicate key" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail="Practice exam already exists with these parameters"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Failed to create practice exam: {error_msg}"
                    )
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to create practice exam"
                )
            except Exception as e:
                conn.rollback()
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail="An unexpected error occurred"
                )
