from fastapi import APIRouter, HTTPException
import psycopg2
from database import get_db
from models import ExamResponse
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