from fastapi import APIRouter, HTTPException
import psycopg2
from database import get_db
from models import UserSignup, UserLogin, UserResponse

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user: UserSignup):
    """Register a new user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO users 
                    (first_name, last_name, email, password, date_of_birth,
                     country_code, phone_number, profile_image, school_name, city, state)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_id, first_name, last_name, email, date_of_birth,
                              country_code, phone_number, profile_image, school_name, 
                              city, state, email_verified, phone_verified, last_login,
                              is_active, created_at, updated_at
                """, (user.first_name, user.last_name, user.email, user.password, 
                       user.date_of_birth, user.country_code, user.phone_number,
                      user.profile_image, user.school_name, user.city, user.state))
                
                new_user = cur.fetchone()
                user_id = new_user['user_id']

                exam_data = [(user_id, exam_id) for exam_id in user.exam_overview_id]

                # Insert multiple rows into user_exams table
                cur.executemany("""
                    INSERT INTO user_exams 
                    (user_id, exam_overview_id)
                    VALUES (%s, %s)
                """, exam_data)

                conn.commit()
                return new_user
                
            except psycopg2.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                print(f"Database Error: {error_msg}")
                
                if "unique constraint" in error_msg.lower() and "email" in error_msg.lower():
                    raise HTTPException(status_code=400, detail="Email already registered")
                else:
                    raise HTTPException(status_code=400, detail=f"Registration failed: {error_msg}")

@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin):
    """Login user"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT user_id, first_name, last_name, email, date_of_birth,
                       country_code, phone_number, profile_image, school_name, 
                       city, state, email_verified, phone_verified, last_login,
                       is_active, created_at, updated_at, password
                FROM users
                WHERE email = %s
            """, (credentials.email,))
            
            user = cur.fetchone()
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            # Check if user is active
            if not user['is_active']:
                raise HTTPException(status_code=403, detail="Account is deactivated")
            
            # Check password
            if user['password'] != credentials.password:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            # Update last_login timestamp
            cur.execute("""
                UPDATE users
                SET last_login = NOW()
                WHERE user_id = %s
            """, (user['user_id'],))
            conn.commit()
            
            # Remove password from response
            user_data = dict(user)
            del user_data['password']
            
            # Update last_login in response
            user_data['last_login'] = user['last_login']
            
            return user_data