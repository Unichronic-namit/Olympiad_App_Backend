from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import Json
from database import get_db
from models import PractceExamAttemptDetailsRequest, PracticeExamAttemptDetailsResponse

router = APIRouter(tags=["Practice Exam Attempt Details"])

@router.put("/practice_exam_attempt_details/{practice_exam_attempt_details_id}", response_model=PracticeExamAttemptDetailsResponse)
def update_practice_exam_attempt_details(
    practice_exam_attempt_details_id: int, 
    practice_exam_attempt_details: PractceExamAttemptDetailsRequest
):
    """Append new question-answer details to the existing array"""
    
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
                    SELECT practice_exam_attempt_details_id 
                    FROM practice_exam_attempt_details 
                    WHERE practice_exam_attempt_details_id = %s
                """, (practice_exam_attempt_details_id,))
                
                if not cur.fetchone():
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Practice exam attempt details with ID {practice_exam_attempt_details_id} not found"
                    )
                
                # Create the new object to append
                new_question_answer = {
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
                
                updated_data = cur.fetchone()
                
                if not updated_data:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to update record"
                    )
                
                conn.commit()
                
                print(f"Successfully updated practice exam attempt details ID: {practice_exam_attempt_details_id}")
                print(f"Appended question_id: {practice_exam_attempt_details.question_id}")
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
