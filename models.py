from pydantic import BaseModel, Field
from typing import Optional, List 
from datetime import datetime, date

# Exam Overview Models
class ExamCreate(BaseModel):
    exam: str = Field(..., max_length=100)
    grade: int = Field(..., ge=1, le=12)
    level: int
    total_questions: int = Field(..., ge=0)
    total_marks: int = Field(..., ge=0)
    total_time_mins: int = Field(..., gt=0)

class ExamUpdate(BaseModel):
    total_marks: Optional[int] = Field(None, ge=0)
    total_time_mins: Optional[int] = Field(None, gt=0)

class ExamResponse(BaseModel):
    exam_overview_id: int
    exam: str
    grade: int
    level: int
    total_questions: int
    total_marks: int
    total_time_mins: int

# Section Models
class SectionCreate(BaseModel):
    section: str = Field(..., max_length=100)
    no_of_questions: int = Field(..., gt=0)
    marks_per_question: int = Field(..., gt=0)
    total_marks: int

class SectionUpdate(BaseModel):
    no_of_questions: Optional[int] = Field(None, gt=0)
    total_marks: Optional[int] = Field(None, gt=0)

class SectionResponse(BaseModel):
    section_id: int
    exam_overview_id: int
    section: str
    no_of_questions: int
    marks_per_question: int
    total_marks: int
    exam: str
    grade: int
    level: int

# Syllabus Models
class SyllabusCreate(BaseModel):
    topic: str = Field(..., max_length=200)
    subtopic: Optional[str] = Field(default="", max_length=200)

class SyllabusUpdate(BaseModel):
    topic: Optional[str] = Field(None, max_length=200)
    subtopic: Optional[str] = Field(None, max_length=200)

class SyllabusResponse(BaseModel):
    syllabus_id: int
    exam_overview_id: int
    section_id: int
    topic: str
    subtopic: Optional[str] = None

# Notes Models
class NoteCreate(BaseModel):
    note: str

class NoteUpdate(BaseModel):
    note: str

class NoteResponse(BaseModel):
    note_id: int
    note: str
    exam_overview_id: int

# Question Models
class QuestionCreate(BaseModel):
    difficulty: str = Field(..., max_length=20)
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str = Field(..., max_length=5)
    solution: str = ""

class QuestionUpdate(BaseModel):
    solution: Optional[str] = None

class QuestionResponse(BaseModel):
    question_id: int
    syllabus_id: int
    difficulty: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    solution: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    question_image_url: Optional[str] = None
    option_a_image_url: Optional[str] = None
    option_b_image_url: Optional[str] = None
    option_c_image_url: Optional[str] = None
    option_d_image_url: Optional[str] = None

# # Bulk Upload Model
# class BulkUploadRequest(BaseModel):
#     questions: List[QuestionCreate]

# # AI Generate Model
# class AIGenerateRequest(BaseModel):
#     exam: str
#     grade: int
#     level: int
#     section_id: int

# User Models
class UserSignup(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)
    grade: Optional[int] = Field(None, ge=1, le=12)
    date_of_birth: Optional[date] = None
    country_code: Optional[str] = Field(None, max_length=5)
    phone_number: Optional[str] = Field(None, max_length=20)
    profile_image: Optional[str] = None
    school_name: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    exam_overview_id: List[int] = Field(..., min_items=1)

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    # grade: Optional[int]
    date_of_birth: Optional[date]
    country_code: Optional[str]
    phone_number: Optional[str]
    profile_image: Optional[str]
    school_name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    email_verified: bool
    phone_verified: bool
    last_login: Optional[datetime]  # Changed from str to datetime
    is_active: bool
    created_at: datetime  # Changed from str to datetime
    updated_at: datetime  # Changed from str to datetime

class UserInfoResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    date_of_birth: Optional[date]
    country_code: Optional[str]
    phone_number: Optional[str]
    profile_image: Optional[str]
    school_name: Optional[str]
    city: Optional[str]
    state: Optional[str]

class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    country_code: Optional[str]
    phone_number: Optional[str]
    profile_image: Optional[str]
    school_name: Optional[str]
    city: Optional[str]
    state: Optional[str]

class UserUpdateResponse(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    country_code: Optional[str]
    phone_number: Optional[str]
    profile_image: Optional[str]
    school_name: Optional[str]
    city: Optional[str]
    state: Optional[str]

class UserExamRequest(BaseModel):
    exam_overview_ids: List[int]  # Array of exam IDs to add

class UserExamResponse(BaseModel):
    user_exam_id: int
    user_id: int
    exam_overview_id: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: int

class UserPracticeExamRequest(BaseModel):
    user_id: int
    exam_overview_id: int
    section_id: int
    syllabus_id: Optional[int] = None
    difficulty: Optional[str] = None

class UserPracticeExamResponse(BaseModel):
    user_practice_exam_id: int  # Add this field
    user_id: int
    exam_overview_id: int
    section_id: int
    syllabus_id: int
    difficulty: str
    attempt_count: int
    practice_exam_attempt_details_id: int  # Add this field
    created_at: datetime  # Optional: add if you want to include it

class PracticeExamAttemptDetailsRequest(BaseModel):
    question_id: int
    status: int
    selected_answer: Optional[str] = None 

class PracticeExamAttemptDetailsResponse(BaseModel):
    practice_exam_attempt_details_id: int
    user_practice_exam_id: int
    que_ans_details: List[dict]
    score: int
    total_time: int
    start_time: datetime
    end_time: Optional[datetime]

# Nested model for practice exam attempt details
class PracticeExamAttemptDetailsNested(BaseModel):
    practice_exam_attempt_details_id: int
    user_practice_exam_id: int
    que_ans_details: List[dict]
    score: int
    total_time: int
    start_time: datetime
    end_time: Optional[datetime]

class QuestionAnswerDetail(BaseModel):
    status: int
    question_id: int
    selected_answer: Optional[str]

# Request model - only fields to update
class PracticeExamAttemptDetailsUpdateRequest(BaseModel):
    score: Optional[int] = None
    total_time: Optional[int] = None
    end_time: Optional[datetime] = None

# Nested model for user_practice_exam
class UserPracticeExamNested(BaseModel):
    user_practice_exam_id: int
    user_id: int
    exam_overview_id: int
    section_id: int
    syllabus_id: int
    difficulty: str
    attempt_count: int
    created_at: datetime

# Response model with nested user_practice_exam
class PracticeExamAttemptDetailsFullResponse(BaseModel):
    practice_exam_attempt_details_id: int
    user_practice_exam_id: int
    que_ans_details: List[dict]
    score: int
    total_time: int
    start_time: datetime
    end_time: Optional[datetime]
    user_practice_exam: UserPracticeExamNested

class SectionNested(BaseModel):
    section_id: int
    section: str  # Adjust field names based on your table structure
    # Add other fields from sections table

class SyllabusNested(BaseModel):
    syllabus_id: int
    subtopic: Optional[str]  # Adjust field names based on your table structure
    topic: Optional[str] = None
    # Add other fields from syllabus table

# Add new nested model for questions
class QuestionsNested(BaseModel):
    question_ids: List[int]

class PracticeExamAttemptDetailsNested(BaseModel):
    practice_exam_attempt_details_id: int
    user_practice_exam_id: int
    que_ans_details: List[dict]
    score: int
    total_time: int
    start_time: datetime
    end_time: Optional[datetime]

class UserPracticeExamGetResponse(BaseModel):
    user_practice_exam_id: int
    user_id: int
    exam_overview_id: int
    section_id: int
    syllabus_id: int
    difficulty: str
    attempt_count: int
    created_at: datetime
    practice_exam_attempt_details: PracticeExamAttemptDetailsNested
    exam_overview: ExamResponse  # Added
    section: SectionNested  # Added
    syllabus: SyllabusNested  # Added
    questions: QuestionsNested  # Added

class StatisticsSummary(BaseModel):
    total_time: int  # Sum of all total_time
    best_score: int  # Highest score
    average_score: float  # Average of all scores
    total_attempts: int  # Total number of attempts

class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class UserPracticeExamPaginatedResponse(BaseModel):
    data: List[UserPracticeExamGetResponse]
    pagination: PaginationMeta
    statistics: StatisticsSummary  # Add statistics