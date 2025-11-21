from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import Json
import json
from database import get_db
from models import PracticeExamAttemptDetailsRequest, PracticeExamAttemptDetailsResponse, QuestionAnswerDetail, PracticeExamAttemptDetailsFullResponse, PracticeExamAttemptDetailsUpdateRequest
from typing import List

router = APIRouter(tags=["Practice Exam Attempt Details"])

@router.put("/practice_exam_attempt_details/{practice_exam_attempt_details_id}", response_model=PracticeExamAttemptDetailsResponse)
def update_practice_exam_attempt_details(
    practice_exam_attempt_details_id: int, 
    practice_exam_attempt_details: PracticeExamAttemptDetailsRequest
):
    """Update or append question-answer details"""

    print(f"Received update request for practice_exam_attempt_details_id: {practice_exam_attempt_details_id}")
    print(f"Request body: {practice_exam_attempt_details}")
    
    # Validate input
    if not practice_exam_attempt_details.question_id:
        raise HTTPException(
            status_code=400,
            detail="question_id is required"
        )
    
    if practice_exam_attempt_details.status is None:
        raise HTTPException(
            status_code=400,
            detail="status is required"
        )
    
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Check if record exists
                cur.execute("""
                    SELECT practice_exam_attempt_details_id, que_ans_details
                    FROM practice_exam_attempt_details 
                    WHERE practice_exam_attempt_details_id = %s
                """, (practice_exam_attempt_details_id,))
                
                record = cur.fetchone()
                
                if not record:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Practice exam attempt details with ID {practice_exam_attempt_details_id} not found"
                    )
                
                # Get current que_ans_details array
                current_que_ans_details = record['que_ans_details'] or []
                
                # Check if question_id already exists in the array
                question_exists = False
                question_index = -1
                
                for idx, item in enumerate(current_que_ans_details):
                    if item.get('question_id') == practice_exam_attempt_details.question_id:
                        question_exists = True
                        question_index = idx
                        break
                
                if question_exists:
                    # Question exists - check status
                    if practice_exam_attempt_details.status == 2 or practice_exam_attempt_details.status == 1:
                        # Status is 0 - only update status and selected_answer
                        current_que_ans_details[question_index]['status'] = practice_exam_attempt_details.status
                        current_que_ans_details[question_index]['selected_answer'] = practice_exam_attempt_details.selected_answer
                        print(f"Updated existing question_id {practice_exam_attempt_details.question_id} with status 0")
                    else:
                        # Status is not 0 - don't create new, just skip
                        print(f"Question_id {practice_exam_attempt_details.question_id} already exists. Skipping.")
                        
                    # Update the array in database
                    cur.execute("""
                        UPDATE practice_exam_attempt_details
                        SET que_ans_details = %s::jsonb
                        WHERE practice_exam_attempt_details_id = %s
                        RETURNING practice_exam_attempt_details_id, user_practice_exam_id, 
                                  que_ans_details, score, total_time, start_time, end_time
                    """, (
                        json.dumps(current_que_ans_details),
                        practice_exam_attempt_details_id
                    ))
                else:
                    # Question doesn't exist - append new entry
                    new_question_answer = {
                        "question_no": practice_exam_attempt_details.question_no,
                        "question_id": practice_exam_attempt_details.question_id,
                        "status": practice_exam_attempt_details.status,
                        "selected_answer": practice_exam_attempt_details.selected_answer
                    }
                    
                    # Append to que_ans_details array using || operator
                    cur.execute("""
                        UPDATE practice_exam_attempt_details
                        SET que_ans_details = COALESCE(que_ans_details, '[]'::jsonb) || %s::jsonb
                        WHERE practice_exam_attempt_details_id = %s
                        RETURNING practice_exam_attempt_details_id, user_practice_exam_id, 
                                  que_ans_details, score, total_time, start_time, end_time
                    """, (
                        Json(new_question_answer),
                        practice_exam_attempt_details_id
                    ))
                    
                    print(f"Appended new question_id: {practice_exam_attempt_details.question_id}")
                
                updated_data = cur.fetchone()
                
                if not updated_data:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to update record"
                    )
                
                conn.commit()
                
                print(f"Successfully updated practice exam attempt details ID: {practice_exam_attempt_details_id}")
                print(f"Current array length: {len(updated_data['que_ans_details'])}")
                
                return updated_data
                
            except HTTPException:
                conn.rollback()
                raise
                
            except psycopg2.DataError as e:
                conn.rollback()
                print(f"Data Error: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid data format: {str(e)}"
                )
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Integrity Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(
                        status_code=400,
                        detail="Foreign key constraint violation"
                    )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Database integrity error: {error_msg}"
                    )
                    
            except psycopg2.OperationalError as e:
                conn.rollback()
                print(f"Operational Error: {str(e)}")
                raise HTTPException(
                    status_code=503,
                    detail="Database connection error. Please try again later."
                )
                
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Database error occurred: {str(e)}"
                )
                
            except ValueError as e:
                conn.rollback()
                print(f"Value Error: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid value provided: {str(e)}"
                )
                
            except Exception as e:
                conn.rollback()
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while updating the record"
                )

@router.get("/practice_exam_attempt_details/{practice_exam_attempt_details_id}", response_model=List[QuestionAnswerDetail])
def get_practice_exam_attempt_details(practice_exam_attempt_details_id: int):
    """Get question-answer details for a specific practice exam attempt"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Fetch the que_ans_details array
                cur.execute("""
                    SELECT que_ans_details
                    FROM practice_exam_attempt_details
                    WHERE practice_exam_attempt_details_id = %s
                """, (practice_exam_attempt_details_id,))
                
                record = cur.fetchone()
                
                # If record not found, raise 404
                if not record:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Practice exam attempt details with ID {practice_exam_attempt_details_id} not found"
                    )
                
                # Get the que_ans_details array
                que_ans_details = record['que_ans_details'] or []
                
                print(f"Retrieved {len(que_ans_details)} question-answer details for ID: {practice_exam_attempt_details_id}")
                
                # Return the array directly
                return que_ans_details
                
            except HTTPException:
                # Re-raise HTTP exceptions
                raise
                
            except psycopg2.Error as e:
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve practice exam attempt details"
                )
                
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred"
                )

@router.put("/practice_exam_attempt_details_finish/{practice_exam_attempt_details_id}", 
            response_model=PracticeExamAttemptDetailsFullResponse)
def update_practice_exam_attempt_details_final(
    practice_exam_attempt_details_id: int,
    update_data: PracticeExamAttemptDetailsUpdateRequest
):
    """Update score, total_time, and end_time for practice exam attempt"""
    
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Check if record exists
                cur.execute("""
                    SELECT practice_exam_attempt_details_id
                    FROM practice_exam_attempt_details
                    WHERE practice_exam_attempt_details_id = %s
                """, (practice_exam_attempt_details_id,))
                
                if not cur.fetchone():
                    raise HTTPException(
                        status_code=404,
                        detail=f"Practice exam attempt details with ID {practice_exam_attempt_details_id} not found"
                    )
                
                # Build dynamic UPDATE query for only provided fields
                update_fields = []
                params = []
                
                if update_data.score is not None:
                    update_fields.append("score = %s")
                    params.append(update_data.score)
                
                if update_data.total_time is not None:
                    update_fields.append("total_time = %s")
                    params.append(update_data.total_time)
                
                if update_data.end_time is not None:
                    update_fields.append("end_time = %s")
                    params.append(update_data.end_time)
                
                # If no fields to update, just fetch current data
                if not update_fields:
                    # Just fetch without updating
                    params.append(practice_exam_attempt_details_id)
                else:
                    # Update the record
                    params.append(practice_exam_attempt_details_id)
                    
                    update_query = f"""
                        UPDATE practice_exam_attempt_details
                        SET {', '.join(update_fields)}
                        WHERE practice_exam_attempt_details_id = %s
                    """
                    
                    cur.execute(update_query, params)
                    conn.commit()
                    print(f"Updated practice exam attempt details ID: {practice_exam_attempt_details_id}")
                
                # Fetch the complete data with JOIN
                cur.execute("""
                    SELECT 
                        pead.practice_exam_attempt_details_id,
                        pead.user_practice_exam_id,
                        pead.que_ans_details,
                        pead.score,
                        pead.total_time,
                        pead.start_time,
                        pead.end_time,
                        upe.user_practice_exam_id as upe_id,
                        upe.user_id,
                        upe.exam_overview_id,
                        upe.section_id,
                        upe.syllabus_id,
                        upe.difficulty,
                        upe.attempt_count,
                        upe.created_at as upe_created_at
                    FROM practice_exam_attempt_details pead
                    INNER JOIN user_practice_exam upe
                        ON pead.user_practice_exam_id = upe.user_practice_exam_id
                    WHERE pead.practice_exam_attempt_details_id = %s
                """, (practice_exam_attempt_details_id,))
                
                result = cur.fetchone()
                
                if not result:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to retrieve updated record"
                    )
                
                # Structure the nested response
                response = {
                    "practice_exam_attempt_details_id": result['practice_exam_attempt_details_id'],
                    "user_practice_exam_id": result['user_practice_exam_id'],
                    "que_ans_details": result['que_ans_details'],
                    "score": result['score'],
                    "total_time": result['total_time'],
                    "start_time": result['start_time'],
                    "end_time": result['end_time'],
                    "user_practice_exam": {
                        "user_practice_exam_id": result['upe_id'],
                        "user_id": result['user_id'],
                        "exam_overview_id": result['exam_overview_id'],
                        "section_id": result['section_id'],
                        "syllabus_id": result['syllabus_id'],
                        "difficulty": result['difficulty'],
                        "attempt_count": result['attempt_count'],
                        "created_at": result['upe_created_at']
                    }
                }
                
                print(f"Retrieved complete data for practice exam attempt details ID: {practice_exam_attempt_details_id}")
                
                return response
                
            except HTTPException:
                conn.rollback()
                raise
                
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to update practice exam attempt details"
                )
                
            except Exception as e:
                conn.rollback()
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred"
                )
