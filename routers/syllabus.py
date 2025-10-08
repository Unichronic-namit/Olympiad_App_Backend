from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from database import get_db
from models import SyllabusCreate, SyllabusUpdate, SyllabusResponse

router = APIRouter(tags=["Syllabus"])

@router.get("/sections/{section_id}/syllabus", response_model=List[SyllabusResponse])
def get_syllabus_list(section_id: int):
    """Get syllabus list for a section"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Check if section exists
            cur.execute("SELECT 1 FROM sections WHERE section_id = %s", (section_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Section not found")
            
            cur.execute("""
                SELECT syllabus_id, exam_overview_id, section_id, topic, subtopic
                FROM syllabus
                WHERE section_id = %s
                ORDER BY syllabus_id
            """, (section_id,))
            
            syllabus_list = cur.fetchall()
            return syllabus_list

@router.post("/sections/{section_id}/syllabus", response_model=SyllabusResponse, status_code=201)
def add_topic_subtopic(section_id: int, syllabus: SyllabusCreate):
    """Add new topic/subtopic"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # First, fetch exam_overview_id from sections table
                cur.execute("""
                    SELECT exam_overview_id 
                    FROM sections 
                    WHERE section_id = %s
                """, (section_id,))
                
                section_data = cur.fetchone()
                
                if not section_data:
                    raise HTTPException(status_code=404, detail="Section not found")
                
                exam_overview_id = section_data['exam_overview_id']
                
                # Now insert into syllabus table
                cur.execute("""
                    INSERT INTO syllabus 
                    (exam_overview_id, section_id, topic, subtopic)
                    VALUES (%s, %s, %s, %s)
                    RETURNING syllabus_id, exam_overview_id, section_id, topic, subtopic
                """, (exam_overview_id, section_id, syllabus.topic, syllabus.subtopic))
                
                new_syllabus = cur.fetchone()
                conn.commit()
                return new_syllabus
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "foreign key" in error_msg.lower():
                    raise HTTPException(status_code=404, detail="Section or Exam not found")
                elif "unique constraint" in error_msg.lower():
                    raise HTTPException(status_code=400, detail="Topic/Subtopic already exists")
                else:
                    raise HTTPException(status_code=400, detail=f"Database constraint violation: {error_msg}")

@router.put("/syllabus/{syllabus_id}", response_model=SyllabusResponse)
def update_topic_subtopic(syllabus_id: int, syllabus: SyllabusUpdate):
    """Update topic/subtopic"""
    with get_db() as conn:
        with conn.cursor() as cur:
            updates = []
            values = []
            
            if syllabus.topic is not None:
                updates.append("topic = %s")
                values.append(syllabus.topic)
            
            if syllabus.subtopic is not None:
                updates.append("subtopic = %s")
                values.append(syllabus.subtopic)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            values.append(syllabus_id)
            
            cur.execute(f"""
                UPDATE syllabus
                SET {', '.join(updates)}
                WHERE syllabus_id = %s
                RETURNING syllabus_id, exam_overview_id, section_id, topic, subtopic
            """, values)
            
            updated_syllabus = cur.fetchone()
            
            if not updated_syllabus:
                raise HTTPException(status_code=404, detail="Syllabus entry not found")
            
            conn.commit()
            return updated_syllabus

@router.delete("/syllabus/{syllabus_id}", status_code=204)
def delete_topic_subtopic(syllabus_id: int):
    """Delete topic/subtopic"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM syllabus
                WHERE syllabus_id = %s
            """, (syllabus_id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Syllabus entry not found")
            
            conn.commit()