from fastapi import APIRouter, HTTPException
import psycopg2
from database import get_db
from models import UserInfoResponse, UserUpdateRequest, UserUpdateResponse

router = APIRouter(tags=["User Info"])

@router.get("/user_info/{user_id}", response_model=UserInfoResponse)
def get_user_info(user_id: int):
    """Get user information by user_id"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT 
                        first_name,
                        last_name,
                        email,
                        date_of_birth,
                        country_code,
                        phone_number,
                        profile_image,
                        school_name,
                        city,
                        state
                    FROM users
                    WHERE user_id = %s AND is_active = TRUE
                """, (user_id,))
                
                user = cur.fetchone()
                
                if not user:
                    raise HTTPException(
                        status_code=404, 
                        detail="User not found or inactive"
                    )
                
                return user
                
            except psycopg2.Error as e:
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to fetch user information"
                )

@router.put("/user_info/{user_id}", response_model=UserUpdateResponse)
def update_user_info(user_id: int, user_data: UserUpdateRequest):
    """Update user information by user_id"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                # First check if user exists
                cur.execute("""
                    SELECT user_id FROM users 
                    WHERE user_id = %s AND is_active = TRUE
                """, (user_id,))
                
                if not cur.fetchone():
                    raise HTTPException(
                        status_code=404, 
                        detail="User not found or inactive"
                    )
                
                # Update user information
                cur.execute("""
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s,
                        date_of_birth = %s,
                        country_code = %s,
                        phone_number = %s,
                        profile_image = %s,
                        school_name = %s,
                        city = %s,
                        state = %s,
                        updated_at = NOW()
                    WHERE user_id = %s AND is_active = TRUE
                    RETURNING first_name, last_name, date_of_birth,
                              country_code, phone_number, profile_image,
                              school_name, city, state
                """, (
                    user_data.first_name,
                    user_data.last_name,
                    user_data.date_of_birth,
                    user_data.country_code,
                    user_data.phone_number,
                    user_data.profile_image,
                    user_data.school_name,
                    user_data.city,
                    user_data.state,
                    user_id
                ))
                
                updated_user = cur.fetchone()
                conn.commit()
                
                print(f"User {user_id} updated successfully")
                return updated_user
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "unique constraint" in error_msg.lower() and "email" in error_msg.lower():
                    raise HTTPException(
                        status_code=400, 
                        detail="Email already exists"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Update failed: {error_msg}"
                    )
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Database Error: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to update user information"
                )