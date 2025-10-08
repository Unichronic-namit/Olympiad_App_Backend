from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
import psycopg2
from database import get_db
from models import QuestionCreate, QuestionUpdate, QuestionResponse

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
                       solution, is_active, created_at, updated_at
                FROM questions
                WHERE syllabus_id = %s AND is_active = TRUE
                ORDER BY question_id
            """, (syllabus_id,))
            
            questions = cur.fetchall()
            return questions

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