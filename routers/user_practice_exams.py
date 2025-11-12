from fastapi import APIRouter, HTTPException, Query
import psycopg2
import json
from database import get_db
from models import UserPracticeExamRequest, UserPracticeExamResponse, UserPracticeExamPaginatedResponse
from datetime import datetime
import math
from typing import Optional

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
                        (user_id, exam_overview_id, section_id, syllabus_id, difficulty, attempt_count)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING *
                    """, (request.user_id, request.exam_overview_id, request.section_id, 
                          request.syllabus_id, request.difficulty, 1))
                    
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

@router.get("/user_practice_exam/{user_id}", response_model=UserPracticeExamPaginatedResponse)
def get_user_practice_exams(
    user_id: int,
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level (easy, medium, hard)"),
    search: Optional[str] = Query(None, description="Search in exam name, section, topic, or subtopic")
):
    """Get paginated practice exams with search, filters, and statistics"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Build WHERE clause based on filters
                where_conditions = ["upe.user_id = %s"]
                count_params = [user_id]
                query_params = [user_id]
                stats_params = [user_id]
                
                # Add difficulty filter if provided
                if difficulty:
                    where_conditions.append("upe.difficulty = %s")
                    count_params.append(difficulty)
                    query_params.append(difficulty)
                    stats_params.append(difficulty)
                
                # Add search filter if provided
                if search:
                    search_condition = """(
                        LOWER(eo.exam) LIKE LOWER(%s) OR
                        LOWER(s.section) LIKE LOWER(%s) OR
                        LOWER(sy.topic) LIKE LOWER(%s) OR
                        LOWER(sy.subtopic) LIKE LOWER(%s)
                    )"""
                    where_conditions.append(search_condition)
                    search_term = f"%{search}%"
                    count_params.extend([search_term, search_term, search_term, search_term])
                    query_params.extend([search_term, search_term, search_term, search_term])
                    stats_params.extend([search_term, search_term, search_term, search_term])
                
                where_clause = " AND ".join(where_conditions)
                
                # Get aggregate statistics
                stats_query = f"""
                    SELECT 
                        COALESCE(SUM(pead.total_time), 0) as total_time,
                        COALESCE(MAX(pead.score), 0) as best_score,
                        COALESCE(AVG(pead.score), 0) as average_score,
                        COUNT(pead.practice_exam_attempt_details_id) as total_attempts
                    FROM user_practice_exam upe
                    INNER JOIN practice_exam_attempt_details pead
                        ON upe.user_practice_exam_id = pead.user_practice_exam_id
                    INNER JOIN exam_overview eo
                        ON upe.exam_overview_id = eo.exam_overview_id
                    INNER JOIN sections s
                        ON upe.section_id = s.section_id
                    INNER JOIN syllabus sy
                        ON upe.syllabus_id = sy.syllabus_id
                    WHERE {where_clause}
                """
                
                cur.execute(stats_query, stats_params)
                stats = cur.fetchone()
                
                total_count = stats['total_attempts']
                
                print(f"Statistics for user ID {user_id}: Total attempts={total_count}, Best score={stats['best_score']}, Avg score={stats['average_score']:.2f}, Total time={stats['total_time']}")
                
                # Calculate pagination values
                total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
                offset = (page - 1) * page_size
                has_next = page < total_pages
                has_previous = page > 1
                
                # Add pagination parameters
                query_params.extend([page_size, offset])
                
                # Join multiple tables with enriched que_ans_details
                main_query = f"""
                    SELECT 
                        -- user_practice_exam fields
                        upe.user_practice_exam_id,
                        upe.user_id,
                        upe.exam_overview_id,
                        upe.section_id,
                        upe.syllabus_id,
                        upe.difficulty,
                        upe.attempt_count,
                        upe.created_at,
                        
                        -- practice_exam_attempt_details fields
                        pead.practice_exam_attempt_details_id,
                        pead.user_practice_exam_id as pead_user_practice_exam_id,
                        
                        -- Enrich que_ans_details with correct_option
                        (
                            SELECT jsonb_agg(
                                elem || jsonb_build_object(
                                    'correct_option', 
                                    COALESCE(q.correct_option, null)
                                )
                            )
                            FROM jsonb_array_elements(pead.que_ans_details) elem
                            LEFT JOIN questions q ON (elem->>'question_id')::int = q.question_id
                        ) as que_ans_details,
                        
                        pead.score,
                        pead.total_time,
                        pead.start_time,
                        pead.end_time,
                        
                        -- exam_overview fields
                        eo.exam_overview_id as eo_id,
                        eo.exam,
                        eo.grade,
                        eo.level,
                        eo.total_questions,
                        eo.total_marks,
                        eo.total_time_mins,
                        
                        -- sections fields
                        s.section_id as s_id,
                        s.section,
                        
                        -- syllabus fields
                        sy.syllabus_id as sy_id,
                        sy.subtopic,
                        sy.topic,
                        
                        -- questions array aggregated by syllabus_id
                        COALESCE(
                            (SELECT ARRAY_AGG(q.question_id ORDER BY q.question_id)
                             FROM questions q
                             WHERE q.syllabus_id = upe.syllabus_id),
                            ARRAY[]::integer[]
                        ) as question_ids
                        
                    FROM user_practice_exam upe
                    INNER JOIN practice_exam_attempt_details pead
                        ON upe.user_practice_exam_id = pead.user_practice_exam_id
                    INNER JOIN exam_overview eo
                        ON upe.exam_overview_id = eo.exam_overview_id
                    INNER JOIN sections s
                        ON upe.section_id = s.section_id
                    INNER JOIN syllabus sy
                        ON upe.syllabus_id = sy.syllabus_id
                    WHERE {where_clause}
                    ORDER BY pead.start_time DESC
                    LIMIT %s OFFSET %s
                """
                
                cur.execute(main_query, query_params)
                rows = cur.fetchall()
                
                # Structure the nested response with all related data
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
                            "que_ans_details": row['que_ans_details'] or [],
                            "score": row['score'],
                            "total_time": row['total_time'],
                            "start_time": row['start_time'],
                            "end_time": row['end_time']
                        },
                        
                        "exam_overview": {
                            "exam_overview_id": row['eo_id'],
                            "exam": row['exam'],
                            "grade": row['grade'],
                            "level": row['level'],
                            "total_questions": row['total_questions'],
                            "total_marks": row['total_marks'],
                            "total_time_mins": row['total_time_mins']
                        },
                        
                        "section": {
                            "section_id": row['s_id'],
                            "section": row['section']
                        },
                        
                        "syllabus": {
                            "syllabus_id": row['sy_id'],
                            "subtopic": row['subtopic'],
                            "topic": row['topic']
                        },
                        
                        "questions": {
                            "question_ids": row['question_ids'] or []
                        }
                    }
                    result.append(practice_exam)
                
                # Create pagination metadata
                pagination_meta = {
                    "total": total_count,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "has_next": has_next,
                    "has_previous": has_previous
                }
                
                # Create statistics metadata
                statistics_meta = {
                    "total_time": stats['total_time'],
                    "best_score": stats['best_score'],
                    "average_score": round(float(stats['average_score']), 2),
                    "total_attempts": total_count
                }
                
                print(f"Retrieved page {page} with {len(result)} attempt(s) for user ID: {user_id}")
                
                # Return paginated response with statistics
                return {
                    "data": result,
                    "pagination": pagination_meta,
                    "statistics": statistics_meta
                }
                
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