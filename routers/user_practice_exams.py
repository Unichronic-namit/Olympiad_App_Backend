from fastapi import APIRouter, HTTPException
import psycopg2
import json
from database import get_db
from models import UserPracticeExamRequest, UserPracticeExamResponse, UserPracticeExamGetResponse
from typing import List
from datetime import datetime

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
                
                # Check if record already exists
                cur.execute("""
                    SELECT *
                    FROM user_practice_exam
                    WHERE user_id = %s
                        AND exam_overview_id = %s
                        AND section_id = %s
                        AND syllabus_id = %s
                        AND difficulty = %s
                """, (request.user_id, request.exam_overview_id, request.section_id, 
                      request.syllabus_id, request.difficulty))
                
                existing_record = cur.fetchone()
                
                if existing_record:
                    # Use existing record
                    cur.execute("""
                        UPDATE user_practice_exam
                        SET attempt_count = %s
                        WHERE user_practice_exam_id = %s
                    """, (existing_record['attempt_count'] + 1,existing_record['user_practice_exam_id']))
                    user_practice_exam_data = existing_record
                    user_practice_exam_id = existing_record['user_practice_exam_id']
                    created_at = existing_record['created_at']
                    print(f"Using existing practice exam with ID: {user_practice_exam_id}")
                else:
                    # Insert into user_practice_exam table
                    cur.execute("""
                        INSERT INTO user_practice_exam
                        (user_id, exam_overview_id, section_id, syllabus_id, difficulty)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING *
                    """, (request.user_id, request.exam_overview_id, request.section_id, 
                          request.syllabus_id, request.difficulty))
                    
                    user_practice_exam_data = cur.fetchone()
                    user_practice_exam_id = user_practice_exam_data['user_practice_exam_id']
                    created_at = user_practice_exam_data['created_at']
                    print(f"Created new practice exam with ID: {user_practice_exam_id}")
                
                # Insert into practice_exam_attempt_details table
                cur.execute("""
                    INSERT INTO practice_exam_attempt_details
                    (user_practice_exam_id, que_ans_details, score, total_time, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (user_practice_exam_id, json.dumps([]), 0, 0, datetime.utcnow(), None))
                
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
                    **user_practice_exam_data,
                    'practice_exam_attempt_details_id': practice_exam_attempt_details_id
                }
                
                return combined_response
                
            except HTTPException:
                # Re-raise HTTP exceptions
                conn.rollback()
                raise
                
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
                        status_code=409, 
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

@router.get("/user_practice_exam/{user_id}", response_model=List[UserPracticeExamGetResponse])
def get_user_practice_exams(user_id: int):
    """Get all practice exams with attempt details for a specific user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Join both tables to get complete data
                cur.execute("""
                    SELECT 
                        upe.user_practice_exam_id,
                        upe.user_id,
                        upe.exam_overview_id,
                        upe.section_id,
                        upe.syllabus_id,
                        upe.difficulty,
                        upe.attempt_count,
                        upe.created_at,
                        pead.practice_exam_attempt_details_id,
                        pead.user_practice_exam_id as pead_user_practice_exam_id,
                        pead.que_ans_details,
                        pead.score,
                        pead.total_time,
                        pead.start_time,
                        pead.end_time
                    FROM user_practice_exam upe
                    LEFT JOIN practice_exam_attempt_details pead
                        ON upe.user_practice_exam_id = pead.user_practice_exam_id
                    WHERE upe.user_id = %s
                    ORDER BY upe.created_at DESC
                """, (user_id,))
                
                rows = cur.fetchall()
                
                # Return empty list if no records found
                if not rows:
                    return []
                
                # Structure the nested response
                result = []
                for row in rows:
                    practice_exam = {
                        "user_practice_exam_id": row['user_practice_exam_id'],
                        "user_id": row['user_id'],
                        "exam_overview_id": row['exam_overview_id'],
                        "section_id": row['section_id'],
                        "syllabus_id": row['syllabus_id'],
                        "difficulty": row['difficulty'],
                        "attempt_count": row['attempt_count'],
                        "created_at": row['created_at'],
                        "practice_exam_attempt_details": {
                            "practice_exam_attempt_details_id": row['practice_exam_attempt_details_id'],
                            "user_practice_exam_id": row['pead_user_practice_exam_id'],
                            "que_ans_details": row['que_ans_details'],
                            "score": row['score'],
                            "total_time": row['total_time'],
                            "start_time": row['start_time'],
                            "end_time": row['end_time']
                        }
                    }
                    result.append(practice_exam)
                
                print(f"Retrieved {len(result)} practice exam(s) with details for user ID: {user_id}")
                
                return result
                
            except psycopg2.Error as e:
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve user practice exams"
                )
                
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred"
                )