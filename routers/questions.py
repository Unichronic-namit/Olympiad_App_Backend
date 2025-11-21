import random
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
import psycopg2
from database import get_db
from models import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionsForSectionResponse

router = APIRouter(tags=["Questions"])

@router.get("/questions", response_model=List[QuestionResponse])
def get_all_questions(
    syllabus_id: Optional[int] = Query(None),
    difficulty: Optional[str] = Query(None)
):
    """Get all questions (filters optional)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            query = """
                SELECT question_id, syllabus_id, difficulty, question_text,
                       option_a, option_b, option_c, option_d, correct_option,
                       solution, is_active, created_at, updated_at
                FROM questions
                WHERE is_active = TRUE
            """
            params = []
            
            if syllabus_id:
                query += " AND syllabus_id = %s"
                params.append(syllabus_id)
            
            if difficulty:
                query += " AND difficulty = %s"
                params.append(difficulty)
            
            query += " ORDER BY question_id"
            
            cur.execute(query, params)
            questions = cur.fetchall()
            return questions

@router.get("/syllabus/{syllabus_id}/questions", response_model=List[QuestionResponse])
def get_questions_for_topic(syllabus_id: int):
    """Get all questions for one topic"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM syllabus WHERE syllabus_id = %s", (syllabus_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Syllabus topic not found")
            
            cur.execute("""
                SELECT question_id, syllabus_id, difficulty, question_text,
                       option_a, option_b, option_c, option_d, correct_option,
                       solution, is_active, created_at, updated_at, question_image_url,
                       option_a_image_url, option_b_image_url, option_c_image_url, option_d_image_url
                FROM questions
                WHERE syllabus_id = %s AND is_active = TRUE
                ORDER BY question_id
            """, (syllabus_id,))
            
            questions = cur.fetchall()
            return questions
        
@router.get("/section/{section_id}/questions", response_model=QuestionsForSectionResponse)
def get_questions_for_section(section_id: int):
    """Get all questions for one section"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # Check if section exists
                cur.execute("SELECT 1 FROM sections WHERE section_id = %s", (section_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Section not found")

                cur.execute("""
                    SELECT eo.exam_overview_id, eo.exam, eo.grade, eo.level, eo.total_questions, eo.total_marks as exam_total_marks, eo.total_time_mins,
                     s.section_id, s.section, s.no_of_questions, s.marks_per_question, s.total_marks 
                     FROM sections s INNER JOIN exam_overview eo
                     ON s.exam_overview_id = eo.exam_overview_id
                     WHERE s.section_id = %s
                """, (section_id,))

                section_exam_overview_data = cur.fetchone()
                print(f"Section exam overview data: {section_exam_overview_data}")

                marks_per_question_section = section_exam_overview_data['marks_per_question']
                total_marks_section = section_exam_overview_data['total_marks']
                no_of_questions_section = section_exam_overview_data['no_of_questions']

                time_for_section = (section_exam_overview_data['total_time_mins'] / section_exam_overview_data['exam_total_marks']) * total_marks_section
                
                # Get all syllabus_ids for this section
                cur.execute("""
                    SELECT syllabus_id FROM syllabus
                    WHERE section_id = %s
                    ORDER BY syllabus_id
                """, (section_id,))
                
                syllabus_ids = cur.fetchall()
                print(f"Found {len(syllabus_ids)} syllabus records for section {section_id}")
                
                if not syllabus_ids:
                    # No syllabus found for this section
                    return []
                
                # Extract syllabus_ids into a list
                syl_ids = [row['syllabus_id'] for row in syllabus_ids]
                print(f"Syllabus IDs: {syl_ids}")
                
                # Fetch all questions for all syllabus_ids in ONE query
                cur.execute("""
                    SELECT 
                        question_id, 
                        syllabus_id, 
                        difficulty, 
                        question_text,
                        option_a, 
                        option_b, 
                        option_c, 
                        option_d, 
                        correct_option,
                        solution, 
                        is_active, 
                        created_at, 
                        updated_at, 
                        question_image_url,
                        option_a_image_url, 
                        option_b_image_url, 
                        option_c_image_url, 
                        option_d_image_url
                    FROM questions
                    WHERE syllabus_id = ANY(%s) AND is_active = TRUE
                    ORDER BY syllabus_id, question_id
                """, (syl_ids,))
                
                questions = cur.fetchall()
                
                print(f"Retrieved {len(questions)} questions for section {section_id}")

                # Randomly select questions if more than required
                if len(questions) > no_of_questions_section:
                    questions = random.sample(questions, no_of_questions_section)
                elif len(questions) < no_of_questions_section:
                    # Handle case where there are fewer questions than required
                    # (You can decide: return all available or raise an error)
                    pass  # For now, just return what's available

                return {
                    "questions": questions,
                    "time_for_section": time_for_section,
                    "marks_per_question_section": marks_per_question_section,
                    "total_marks_section": total_marks_section,
                    "no_of_questions_section": no_of_questions_section
                }
                
            except HTTPException:
                raise
            except psycopg2.Error as e:
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve questions"
                )
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred"
                )

@router.post("/syllabus/{syllabus_id}/questions", response_model=QuestionResponse, status_code=201)
def add_question(syllabus_id: int, question: QuestionCreate):
    """Add a new question"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO questions 
                    (syllabus_id, difficulty, question_text, option_a, option_b,
                     option_c, option_d, correct_option, solution)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING question_id, syllabus_id, difficulty, question_text,
                              option_a, option_b, option_c, option_d, correct_option,
                              solution, is_active, created_at, updated_at
                """, (syllabus_id, question.difficulty, question.question_text,
                      question.option_a, question.option_b, question.option_c,
                      question.option_d, question.correct_option, question.solution))
                
                new_question = cur.fetchone()
                conn.commit()
                return new_question
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(status_code=404, detail="Syllabus topic not found")
                else:
                    raise HTTPException(status_code=400, detail=f"Database constraint violation: {error_msg}")

@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionUpdate):
    """Update question or solution"""
    with get_db() as conn:
        with conn.cursor() as cur:
            if question.solution is None:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            cur.execute("""
                UPDATE questions
                SET solution = %s, updated_at = NOW()
                WHERE question_id = %s
                RETURNING question_id, syllabus_id, difficulty, question_text,
                          option_a, option_b, option_c, option_d, correct_option,
                          solution, is_active, created_at, updated_at
            """, (question.solution, question_id))
            
            updated_question = cur.fetchone()
            
            if not updated_question:
                raise HTTPException(status_code=404, detail="Question not found")
            
            conn.commit()
            return updated_question

@router.delete("/questions/{question_id}", status_code=204)
def delete_question(question_id: int):
    """Delete question"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM questions
                WHERE question_id = %s
            """, (question_id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Question not found")
            
            conn.commit()

# @router.post("/questions/generate", status_code=201)
# def auto_generate_questions(request: AIGenerateRequest):
#     """Auto generate questions using AI"""
#     # TODO: Implement AI generation logic
#     raise HTTPException(status_code=501, detail="AI generation not implemented yet")

# @router.post("/questions/bulk_upload", status_code=201)
# async def bulk_upload_questions(file: UploadFile = File(...)):
#     """Bulk upload questions from JSON or CSV file"""
#     # TODO: Implement bulk upload logic
#     raise HTTPException(status_code=501, detail="Bulk upload not implemented yet")