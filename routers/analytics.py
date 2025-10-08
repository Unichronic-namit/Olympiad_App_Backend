from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import get_db

router = APIRouter(tags=["Combined & Analytics"])

@router.get("/exams/{exam_overview_id}/overview")
def get_full_exam_overview(exam_overview_id: int):
    """Returns exam → sections → syllabus → questions → notes"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get exam
            cur.execute("""
                SELECT exam_overview_id, exam, grade, level,
                       total_questions, total_marks, total_time_mins
                FROM exam_overview
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            exam = cur.fetchone()
            
            if not exam:
                raise HTTPException(status_code=404, detail="Exam not found")
            
            # Get sections
            cur.execute("""
                SELECT section_id, section, no_of_questions,
                       marks_per_question, total_marks
                FROM sections
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            sections = cur.fetchall()
            
            # Get syllabus for each section
            for section in sections:
                cur.execute("""
                    SELECT syllabus_id, topic, subtopic
                    FROM syllabus
                    WHERE section_id = %s
                """, (section['section_id'],))
                section['syllabus'] = cur.fetchall()
                
                # Get questions for each syllabus topic
                for syllabus_item in section['syllabus']:
                    cur.execute("""
                        SELECT question_id, difficulty, question_text,
                               option_a, option_b, option_c, option_d,
                               correct_option, solution
                        FROM questions
                        WHERE syllabus_id = %s AND is_active = TRUE
                    """, (syllabus_item['syllabus_id'],))
                    syllabus_item['questions'] = cur.fetchall()
            
            # Get notes
            cur.execute("""
                SELECT note_id, note
                FROM notes
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            notes = cur.fetchall()
            
            return {
                "exam": exam,
                "sections": sections,
                "notes": notes
            }

@router.get("/analytics/exam/{exam_overview_id}")
def get_exam_analytics(exam_overview_id: int):
    """Count of topics and questions by difficulty"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Check if exam exists
            cur.execute("SELECT 1 FROM exam_overview WHERE exam_overview_id = %s", 
                       (exam_overview_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Exam not found")
            
            # Count total topics
            cur.execute("""
                SELECT COUNT(*) as total_topics
                FROM syllabus
                WHERE exam_overview_id = %s
            """, (exam_overview_id,))
            topic_count = cur.fetchone()
            
            # Count questions by difficulty
            cur.execute("""
                SELECT q.difficulty, COUNT(*) as count
                FROM questions q
                JOIN syllabus s ON q.syllabus_id = s.syllabus_id
                WHERE s.exam_overview_id = %s AND q.is_active = TRUE
                GROUP BY q.difficulty
            """, (exam_overview_id,))
            difficulty_counts = cur.fetchall()
            
            return {
                "exam_overview_id": exam_overview_id,
                "total_topics": topic_count['total_topics'],
                "questions_by_difficulty": difficulty_counts
            }

# @router.get("/search/questions")
# def search_questions(
#     q: Optional[str] = Query(None, description="Search in question text"),
#     grade: Optional[int] = Query(None)
# ):
#     """Search in question bank"""
#     with get_db() as conn:
#         with conn.cursor() as cur:
#             query = """
#                 SELECT q.question_id, q.difficulty, q.question_text,
#                        q.option_a, q.option_b, q.option_c, q.option_d,
#                        s.topic, s.subtopic, e.exam, e.grade
#                 FROM questions q
#                 JOIN syllabus s ON q.syllabus_id = s.syllabus_id
#                 JOIN exam_overview e ON s.exam_overview_id = e.exam_overview_id
#                 WHERE q.is_active = TRUE
#             """
#             params = []
            
#             if q:
#                 query += " AND q.question_text ILIKE %s"
#                 params.append(f"%{q}%")
            
#             if grade:
#                 query += " AND e.grade = %s"
#                 params.append(grade)
            
#             query += " ORDER BY q.question_id LIMIT 100"
            
#             cur.execute(query, params)
#             results = cur.fetchall()
            
#             return {
#                 "total_results": len(results),
#                 "questions": results
#             }