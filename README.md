# 🏆 Olympiad App - Backend API

A comprehensive FastAPI-based REST API for managing olympiad exams, user authentication, practice exams, sections, syllabus, questions, notes, and analytics.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Authentication APIs](#1-authentication-apis)
  - [Exam Overview APIs](#2-exam-overview-apis)
  - [Sections APIs](#3-sections-apis)
  - [Syllabus APIs](#4-syllabus-apis)
  - [Questions APIs](#5-questions-apis)
  - [Notes APIs](#6-notes-apis)
  - [Analytics APIs](#7-analytics-apis)
  - [User Exams APIs](#8-user-exams-apis)
  - [User Info APIs](#9-user-info-apis)
  - [User Practice Exams APIs](#10-user-practice-exams-apis)
  - [Practice Exam Attempt Details APIs](#11-practice-exam-attempt-details-apis)
- [Request/Response Models](#requestresponse-models)
- [Error Handling](#error-handling)
- [CORS Configuration](#cors-configuration)
- [Data Flow](#data-flow)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## ✨ Features

- **User Authentication**: Signup and login with user profile management
- **Exam Management**: Create, read, update, and delete exam overviews
- **Section Management**: Manage exam sections with questions and marks
- **Syllabus Management**: Organize topics and subtopics for each section
- **Question Bank**: Store and manage MCQ questions linked to syllabus topics
- **Notes Management**: Add study material and notes for exams
- **User Exams**: Assign exams to users and track their progress
- **Practice Exams**: Create and manage practice exam attempts with detailed tracking
- **Analytics**: Get statistics on topics and questions by difficulty
- **Pagination**: Paginated responses for large datasets
- **Search & Filters**: Search and filter capabilities across various endpoints
- **Data Validation**: Automatic validation using Pydantic models
- **Error Handling**: Comprehensive error messages for debugging
- **Auto-generated API Docs**: Interactive Swagger UI and ReDoc

## 🛠 Tech Stack

- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.30.6
- **Database**: PostgreSQL
- **Database Driver**: psycopg2-binary 2.9.10
- **Validation**: Pydantic 2.9.2
- **Environment**: python-dotenv 1.0.0
- **Testing UI**: Streamlit 1.26.1 (optional)

## 📁 Project Structure

```
olympiad_app/
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── main.py               # Application entry point with CORS configuration
├── database.py           # Database connection utilities
├── models.py             # Pydantic models for request/response validation
├── app.py                # Streamlit testing UI (optional)
├── render.yaml           # Deployment configuration
└── routers/
    ├── __init__.py       # Router initialization
    ├── auth.py           # Authentication endpoints
    ├── exam_overview.py  # Exam endpoints
    ├── sections.py       # Section endpoints
    ├── syllabus.py       # Syllabus endpoints
    ├── questions.py      # Question endpoints
    ├── notes.py          # Notes endpoints
    ├── analytics.py      # Analytics endpoints
    ├── user_exams.py     # User exam assignment endpoints
    ├── user_info.py      # User profile endpoints
    ├── user_practice_exams.py  # Practice exam management endpoints
    └── practice_exam_attempt_details.py  # Practice exam attempt tracking
```

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Olympiad_App_Backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create `.env` file** in the project root:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=olympiad_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

2. **Update `.env` with your database credentials**

## 🗄️ Database Setup

### 1. Create Database

```sql
CREATE DATABASE olympiad_db;
```

### 2. Create Tables

The database schema includes the following main tables:

- `users` - User accounts and profiles
- `exam_overview` - Exam definitions
- `sections` - Exam sections
- `syllabus` - Topics and subtopics
- `questions` - MCQ questions
- `notes` - Study notes
- `user_exams` - User-exam assignments
- `user_practice_exam` - Practice exam records
- `practice_exam_attempt_details` - Practice exam attempt tracking

Refer to your database migration scripts or schema documentation for the complete table definitions.

## 🏃 Running the Application

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

### Interactive API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API Documentation

### Base URL

All API endpoints are relative to: `http://localhost:8000`

---

### 1. Authentication APIs

#### 1.1 Signup

**Endpoint**: `POST /signup`

**Description**: Register a new user account

**Request Body**:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123",
  "grade": 10,
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "exam_overview_id": [1, 2, 3]
}
```

**Response** (201 Created):

```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "email_verified": false,
  "phone_verified": false,
  "last_login": null,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:

- `400`: Email already registered
- `400`: Registration failed (validation error)

---

#### 1.2 Login

**Endpoint**: `POST /login`

**Description**: Authenticate user and return user profile

**Request Body**:

```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):

```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "email_verified": false,
  "phone_verified": false,
  "last_login": "2024-01-15T10:30:00Z",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:

- `401`: Invalid email or password
- `403`: Account is deactivated

---

### 2. Exam Overview APIs

#### 2.1 Get All Exams

**Endpoint**: `GET /exams`

**Description**: Retrieve all exam overviews

**Response** (200 OK):

```json
[
  {
    "exam_overview_id": 1,
    "exam": "ICSO",
    "grade": 5,
    "level": 1,
    "total_questions": 50,
    "total_marks": 50,
    "total_time_mins": 60
  }
]
```

---

#### 2.2 Get Single Exam

**Endpoint**: `GET /exams/{exam_overview_id}`

**Description**: Get details of a specific exam

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (200 OK):

```json
{
  "exam_overview_id": 1,
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "total_questions": 50,
  "total_marks": 50,
  "total_time_mins": 60
}
```

**Error Responses**:

- `404`: Exam not found

---

#### 2.3 Create Exam

**Endpoint**: `POST /exams`

**Description**: Create a new exam overview

**Request Body**:

```json
{
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "total_questions": 50,
  "total_marks": 50,
  "total_time_mins": 60
}
```

**Response** (201 Created):

```json
{
  "exam_overview_id": 1,
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "total_questions": 50,
  "total_marks": 50,
  "total_time_mins": 60
}
```

**Error Responses**:

- `400`: Database constraint violation (e.g., duplicate exam)

---

#### 2.4 Update Exam

**Endpoint**: `PUT /exams/{exam_overview_id}`

**Description**: Update exam details (only total_marks and total_time_mins)

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Request Body**:

```json
{
  "total_marks": 60,
  "total_time_mins": 75
}
```

**Response** (200 OK):

```json
{
  "exam_overview_id": 1,
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "total_questions": 50,
  "total_marks": 60,
  "total_time_mins": 75
}
```

**Error Responses**:

- `400`: No fields to update
- `404`: Exam not found

---

#### 2.5 Delete Exam

**Endpoint**: `DELETE /exams/{exam_overview_id}`

**Description**: Delete an exam (cascade deletes all related data)

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (204 No Content)

**Error Responses**:

- `404`: Exam not found

---

### 3. Sections APIs

#### 3.1 Get All Sections for Exam

**Endpoint**: `GET /exams/{exam_overview_id}/sections`

**Description**: Get all sections for a specific exam

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (200 OK):

```json
[
  {
    "section_id": 1,
    "exam_overview_id": 1,
    "section": "Computer Basics",
    "no_of_questions": 10,
    "marks_per_question": 1,
    "total_marks": 10,
    "exam": "ICSO",
    "grade": 5,
    "level": 1
  }
]
```

**Error Responses**:

- `404`: Exam not found

---

#### 3.2 Create Section

**Endpoint**: `POST /exams/{exam_overview_id}/sections`

**Description**: Add a new section to an exam

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Request Body**:

```json
{
  "section": "Computer Basics",
  "no_of_questions": 10,
  "marks_per_question": 1,
  "total_marks": 10
}
```

**Important**: `total_marks` must equal `no_of_questions × marks_per_question`

**Response** (201 Created):

```json
{
  "section_id": 1,
  "exam_overview_id": 1,
  "section": "Computer Basics",
  "no_of_questions": 10,
  "marks_per_question": 1,
  "total_marks": 10
}
```

**Error Responses**:

- `400`: Validation failed (total_marks mismatch)
- `400`: Section already exists
- `404`: Exam not found

---

#### 3.3 Update Section

**Endpoint**: `PUT /sections/{section_id}`

**Description**: Update section details

**Path Parameters**:

- `section_id` (integer): ID of the section

**Request Body**:

```json
{
  "no_of_questions": 15,
  "total_marks": 15
}
```

**Response** (200 OK):

```json
{
  "section_id": 1,
  "exam_overview_id": 1,
  "section": "Computer Basics",
  "no_of_questions": 15,
  "marks_per_question": 1,
  "total_marks": 15
}
```

**Error Responses**:

- `400`: No fields to update
- `404`: Section not found

---

#### 3.4 Delete Section

**Endpoint**: `DELETE /sections/{section_id}`

**Description**: Delete a section (cascade deletes syllabus and questions)

**Path Parameters**:

- `section_id` (integer): ID of the section

**Response** (204 No Content)

**Error Responses**:

- `404`: Section not found

---

### 4. Syllabus APIs

#### 4.1 Get Syllabus for Section

**Endpoint**: `GET /sections/{section_id}/syllabus`

**Description**: Get all syllabus topics for a section

**Path Parameters**:

- `section_id` (integer): ID of the section

**Response** (200 OK):

```json
[
  {
    "syllabus_id": 1,
    "exam_overview_id": 1,
    "section_id": 1,
    "topic": "Input Devices",
    "subtopic": "Keyboard, Mouse"
  }
]
```

**Error Responses**:

- `404`: Section not found

---

#### 4.2 Create Topic/Subtopic

**Endpoint**: `POST /sections/{section_id}/syllabus`

**Description**: Add a new topic/subtopic to a section

**Path Parameters**:

- `section_id` (integer): ID of the section

**Request Body**:

```json
{
  "topic": "Input Devices",
  "subtopic": "Keyboard, Mouse"
}
```

**Response** (201 Created):

```json
{
  "syllabus_id": 1,
  "exam_overview_id": 1,
  "section_id": 1,
  "topic": "Input Devices",
  "subtopic": "Keyboard, Mouse"
}
```

**Error Responses**:

- `400`: Topic/Subtopic already exists
- `404`: Section or Exam not found

---

#### 4.3 Update Topic/Subtopic

**Endpoint**: `PUT /syllabus/{syllabus_id}`

**Description**: Update topic or subtopic

**Path Parameters**:

- `syllabus_id` (integer): ID of the syllabus entry

**Request Body**:

```json
{
  "topic": "Output Devices",
  "subtopic": "Monitor, Printer"
}
```

**Response** (200 OK):

```json
{
  "syllabus_id": 1,
  "exam_overview_id": 1,
  "section_id": 1,
  "topic": "Output Devices",
  "subtopic": "Monitor, Printer"
}
```

**Error Responses**:

- `400`: No fields to update
- `404`: Syllabus entry not found

---

#### 4.4 Delete Topic/Subtopic

**Endpoint**: `DELETE /syllabus/{syllabus_id}`

**Description**: Delete a syllabus topic/subtopic

**Path Parameters**:

- `syllabus_id` (integer): ID of the syllabus entry

**Response** (204 No Content)

**Error Responses**:

- `404`: Syllabus entry not found

---

### 5. Questions APIs

#### 5.1 Get All Questions

**Endpoint**: `GET /questions`

**Description**: Get all questions with optional filters

**Query Parameters**:

- `syllabus_id` (integer, optional): Filter by syllabus topic
- `difficulty` (string, optional): Filter by difficulty (easy, medium, hard)

**Example**: `GET /questions?syllabus_id=1&difficulty=easy`

**Response** (200 OK):

```json
[
  {
    "question_id": 1,
    "syllabus_id": 1,
    "difficulty": "easy",
    "question_text": "Which of the following is an input device?",
    "option_a": "Monitor",
    "option_b": "Keyboard",
    "option_c": "Speaker",
    "option_d": "Printer",
    "correct_option": "B",
    "solution": "Keyboard is an input device.",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "question_image_url": null,
    "option_a_image_url": null,
    "option_b_image_url": null,
    "option_c_image_url": null,
    "option_d_image_url": null
  }
]
```

---

#### 5.2 Get Questions for Topic

**Endpoint**: `GET /syllabus/{syllabus_id}/questions`

**Description**: Get all questions for a specific syllabus topic

**Path Parameters**:

- `syllabus_id` (integer): ID of the syllabus topic

**Response** (200 OK):

```json
[
  {
    "question_id": 1,
    "syllabus_id": 1,
    "difficulty": "easy",
    "question_text": "Which of the following is an input device?",
    "option_a": "Monitor",
    "option_b": "Keyboard",
    "option_c": "Speaker",
    "option_d": "Printer",
    "correct_option": "B",
    "solution": "Keyboard is an input device.",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "question_image_url": null,
    "option_a_image_url": null,
    "option_b_image_url": null,
    "option_c_image_url": null,
    "option_d_image_url": null
  }
]
```

**Error Responses**:

- `404`: Syllabus topic not found

---

#### 5.3 Get Questions for Section

**Endpoint**: `GET /section/{section_id}/questions`

**Description**: Get all questions for a section with section metadata. Returns random questions based on `no_of_questions_section`.

**Path Parameters**:

- `section_id` (integer): ID of the section

**Response** (200 OK):

```json
{
  "questions": [
    {
      "question_id": 1,
      "syllabus_id": 1,
      "difficulty": "easy",
      "question_text": "Which of the following is an input device?",
      "option_a": "Monitor",
      "option_b": "Keyboard",
      "option_c": "Speaker",
      "option_d": "Printer",
      "correct_option": "B",
      "solution": "Keyboard is an input device.",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "question_image_url": null,
      "option_a_image_url": null,
      "option_b_image_url": null,
      "option_c_image_url": null,
      "option_d_image_url": null
    }
  ],
  "time_for_section": 12.5,
  "marks_per_question_section": 1,
  "total_marks_section": 10,
  "no_of_questions_section": 10
}
```

**Note**: The API randomly selects `no_of_questions_section` questions from all available questions in the section.

**Error Responses**:

- `404`: Section not found
- `500`: Failed to retrieve questions

---

#### 5.4 Add Question

**Endpoint**: `POST /syllabus/{syllabus_id}/questions`

**Description**: Add a new question to a syllabus topic

**Path Parameters**:

- `syllabus_id` (integer): ID of the syllabus topic

**Request Body**:

```json
{
  "difficulty": "easy",
  "question_text": "Which of the following is an input device?",
  "option_a": "Monitor",
  "option_b": "Keyboard",
  "option_c": "Speaker",
  "option_d": "Printer",
  "correct_option": "B",
  "solution": "Keyboard is an input device."
}
```

**Response** (201 Created):

```json
{
  "question_id": 1,
  "syllabus_id": 1,
  "difficulty": "easy",
  "question_text": "Which of the following is an input device?",
  "option_a": "Monitor",
  "option_b": "Keyboard",
  "option_c": "Speaker",
  "option_d": "Printer",
  "correct_option": "B",
  "solution": "Keyboard is an input device.",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:

- `400`: Database constraint violation
- `404`: Syllabus topic not found

---

#### 5.5 Update Question

**Endpoint**: `PUT /questions/{question_id}`

**Description**: Update question solution

**Path Parameters**:

- `question_id` (integer): ID of the question

**Request Body**:

```json
{
  "solution": "Keyboard is an input device used to enter data into a computer."
}
```

**Response** (200 OK):

```json
{
  "question_id": 1,
  "syllabus_id": 1,
  "difficulty": "easy",
  "question_text": "Which of the following is an input device?",
  "option_a": "Monitor",
  "option_b": "Keyboard",
  "option_c": "Speaker",
  "option_d": "Printer",
  "correct_option": "B",
  "solution": "Keyboard is an input device used to enter data into a computer.",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

**Error Responses**:

- `400`: No fields to update
- `404`: Question not found

---

#### 5.6 Delete Question

**Endpoint**: `DELETE /questions/{question_id}`

**Description**: Delete a question

**Path Parameters**:

- `question_id` (integer): ID of the question

**Response** (204 No Content)

**Error Responses**:

- `404`: Question not found

---

### 6. Notes APIs

#### 6.1 Get All Notes for Exam

**Endpoint**: `GET /exams/{exam_overview_id}/notes`

**Description**: Get all notes for a specific exam

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (200 OK):

```json
[
  {
    "note_id": 1,
    "note": "Revise all input and output devices before mock test.",
    "exam_overview_id": 1
  }
]
```

**Error Responses**:

- `404`: Exam not found

---

#### 6.2 Create Note

**Endpoint**: `POST /exams/{exam_overview_id}/notes`

**Description**: Add a new note to an exam

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Request Body**:

```json
{
  "note": "Revise all input and output devices before mock test."
}
```

**Response** (201 Created):

```json
{
  "note_id": 1,
  "note": "Revise all input and output devices before mock test.",
  "exam_overview_id": 1
}
```

**Error Responses**:

- `400`: Database constraint violation
- `404`: Exam not found

---

#### 6.3 Update Note

**Endpoint**: `PUT /notes/{note_id}`

**Description**: Update a note

**Path Parameters**:

- `note_id` (integer): ID of the note

**Request Body**:

```json
{
  "note": "Updated note content."
}
```

**Response** (200 OK):

```json
{
  "note_id": 1,
  "note": "Updated note content.",
  "exam_overview_id": 1
}
```

**Error Responses**:

- `404`: Note not found

---

#### 6.4 Delete Note

**Endpoint**: `DELETE /notes/{note_id}`

**Description**: Delete a note

**Path Parameters**:

- `note_id` (integer): ID of the note

**Response** (204 No Content)

**Error Responses**:

- `404`: Note not found

---

### 7. Analytics APIs

#### 7.1 Get Full Exam Overview

**Endpoint**: `GET /exams/{exam_overview_id}/overview`

**Description**: Get complete exam structure including sections, syllabus, questions, and notes

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (200 OK):

```json
{
  "exam": {
    "exam_overview_id": 1,
    "exam": "ICSO",
    "grade": 5,
    "level": 1,
    "total_questions": 50,
    "total_marks": 50,
    "total_time_mins": 60
  },
  "sections": [
    {
      "section_id": 1,
      "section": "Computer Basics",
      "no_of_questions": 10,
      "marks_per_question": 1,
      "total_marks": 10,
      "syllabus": [
        {
          "syllabus_id": 1,
          "topic": "Input Devices",
          "subtopic": "Keyboard, Mouse",
          "questions": [
            {
              "question_id": 1,
              "difficulty": "easy",
              "question_text": "Which of the following is an input device?",
              "option_a": "Monitor",
              "option_b": "Keyboard",
              "option_c": "Speaker",
              "option_d": "Printer",
              "correct_option": "B",
              "solution": "Keyboard is an input device."
            }
          ]
        }
      ]
    }
  ],
  "notes": [
    {
      "note_id": 1,
      "note": "Revise all input and output devices before mock test."
    }
  ]
}
```

**Error Responses**:

- `404`: Exam not found

---

#### 7.2 Get Exam Analytics

**Endpoint**: `GET /analytics/exam/{exam_overview_id}`

**Description**: Get statistics on topics and questions by difficulty

**Path Parameters**:

- `exam_overview_id` (integer): ID of the exam

**Response** (200 OK):

```json
{
  "exam_overview_id": 1,
  "total_topics": 15,
  "questions_by_difficulty": [
    {
      "difficulty": "easy",
      "count": 20
    },
    {
      "difficulty": "medium",
      "count": 18
    },
    {
      "difficulty": "hard",
      "count": 12
    }
  ]
}
```

**Error Responses**:

- `404`: Exam not found

---

### 8. User Exams APIs

#### 8.1 Get User Exams

**Endpoint**: `GET /user_exam/{user_id}`

**Description**: Get all exams assigned to a user

**Path Parameters**:

- `user_id` (integer): ID of the user

**Response** (200 OK):

```json
[
  {
    "exam_overview_id": 1,
    "exam": "ICSO",
    "grade": 5,
    "level": 1,
    "total_questions": 50,
    "total_marks": 50,
    "total_time_mins": 60
  }
]
```

**Error Responses**:

- `500`: Failed to fetch user exams

---

#### 8.2 Add User Exams

**Endpoint**: `POST /user_exam/{user_id}`

**Description**: Assign exams to a user

**Path Parameters**:

- `user_id` (integer): ID of the user

**Request Body**:

```json
{
  "exam_overview_ids": [1, 2, 3]
}
```

**Response** (201 Created):

```json
[
  {
    "user_exam_id": 1,
    "user_id": 1,
    "exam_overview_id": 1,
    "start_date": null,
    "end_date": null,
    "status": 0
  },
  {
    "user_exam_id": 2,
    "user_id": 1,
    "exam_overview_id": 2,
    "start_date": null,
    "end_date": null,
    "status": 0
  }
]
```

**Error Responses**:

- `400`: Invalid exam_overview_id provided
- `400`: Exam already exists for this user
- `404`: User not found or inactive

---

### 9. User Info APIs

#### 9.1 Get User Info

**Endpoint**: `GET /user_info/{user_id}`

**Description**: Get user profile information

**Path Parameters**:

- `user_id` (integer): ID of the user

**Response** (200 OK):

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra"
}
```

**Error Responses**:

- `404`: User not found or inactive
- `500`: Failed to fetch user information

---

#### 9.2 Update User Info

**Endpoint**: `PUT /user_info/{user_id}`

**Description**: Update user profile information

**Path Parameters**:

- `user_id` (integer): ID of the user

**Request Body**:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra"
}
```

**Response** (200 OK):

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra"
}
```

**Error Responses**:

- `400`: Email already exists
- `400`: Update failed
- `404`: User not found or inactive
- `500`: Failed to update user information

---

### 10. User Practice Exams APIs

#### 10.1 Create Practice Exam

**Endpoint**: `POST /user_practice_exam`

**Description**: Create a new practice exam attempt for a user. If a practice exam with the same parameters exists, it increments the attempt count.

**Request Body**:

```json
{
  "user_id": 1,
  "exam_overview_id": 1,
  "section_id": 1,
  "syllabus_id": 1,
  "difficulty": "easy"
}
```

**Response** (201 Created):

```json
{
  "user_practice_exam_id": 1,
  "user_id": 1,
  "exam_overview_id": 1,
  "section_id": 1,
  "syllabus_id": 1,
  "difficulty": "easy",
  "attempt_count": 1,
  "practice_exam_attempt_details_id": 1,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:

- `400`: Invalid foreign key reference
- `409`: Practice exam already exists with these parameters
- `500`: Failed to create practice exam

---

#### 10.2 Get User Practice Exams (Paginated)

**Endpoint**: `GET /user_practice_exam/{user_id}`

**Description**: Get paginated practice exams for a user with search, filters, statistics, and full questions data. Excludes rows where `syllabus_id = 0` or `difficulty = ''`.

**Path Parameters**:

- `user_id` (integer): ID of the user

**Query Parameters**:

- `page` (integer, default: 1): Page number (starts from 1)
- `page_size` (integer, default: 10, max: 100): Number of items per page
- `difficulty` (string, optional): Filter by difficulty level (easy, medium, hard)
- `search` (string, optional): Search in exam name, section, topic, or subtopic

**Example**: `GET /user_practice_exam/1?page=1&page_size=10&difficulty=easy&search=computer`

**Response** (200 OK):

```json
{
  "data": [
    {
      "user_practice_exam_id": 1,
      "user_id": 1,
      "exam_overview_id": 1,
      "section_id": 1,
      "syllabus_id": 1,
      "difficulty": "easy",
      "attempt_count": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "practice_exam_attempt_details": {
        "practice_exam_attempt_details_id": 1,
        "user_practice_exam_id": 1,
        "que_ans_details": [],
        "score": 0,
        "total_time": 0,
        "start_time": "2024-01-15T10:30:00Z",
        "end_time": null
      },
      "exam_overview": {
        "exam_overview_id": 1,
        "exam": "ICSO",
        "grade": 5,
        "level": 1,
        "total_questions": 50,
        "total_marks": 50,
        "total_time_mins": 60
      },
      "section": {
        "section_id": 1,
        "section": "Computer Basics"
      },
      "syllabus": {
        "syllabus_id": 1,
        "subtopic": "Keyboard, Mouse",
        "topic": "Input Devices"
      },
      "questions": {
        "questions_data": [
          {
            "question_id": 1,
            "syllabus_id": 1,
            "difficulty": "easy",
            "question_text": "Which of the following is an input device?",
            "option_a": "Monitor",
            "option_b": "Keyboard",
            "option_c": "Speaker",
            "option_d": "Printer",
            "correct_option": "B",
            "solution": "Keyboard is an input device.",
            "question_image_url": null,
            "option_a_image_url": null,
            "option_b_image_url": null,
            "option_c_image_url": null,
            "option_d_image_url": null
          }
        ]
      }
    }
  ],
  "pagination": {
    "total": 25,
    "page": 1,
    "page_size": 10,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  },
  "statistics": {
    "total_time": 3600,
    "best_score": 95.5,
    "average_score": 78.2,
    "total_attempts": 25
  }
}
```

**Error Responses**:

- `500`: Failed to retrieve user practice exams

---

#### 10.3 Get User Practice Section Exams (Paginated)

**Endpoint**: `GET /user_practice_section_exam/{user_id}`

**Description**: Get paginated practice section exams for a user. No difficulty filter. Search only in exam and section. Only includes rows where `syllabus_id = 0` AND `difficulty = ''`. Excludes syllabus and questions in response.

**Path Parameters**:

- `user_id` (integer): ID of the user

**Query Parameters**:

- `page` (integer, default: 1): Page number (starts from 1)
- `page_size` (integer, default: 10, max: 100): Number of items per page
- `search` (string, optional): Search in exam name or section only

**Example**: `GET /user_practice_section_exam/1?page=1&page_size=10&search=computer`

**Response** (200 OK):

```json
{
  "data": [
    {
      "user_practice_exam_id": 1,
      "user_id": 1,
      "exam_overview_id": 1,
      "section_id": 1,
      "syllabus_id": 0,
      "difficulty": "",
      "attempt_count": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "practice_exam_attempt_details": {
        "practice_exam_attempt_details_id": 1,
        "user_practice_exam_id": 1,
        "que_ans_details": [],
        "score": 0,
        "total_time": 0,
        "start_time": "2024-01-15T10:30:00Z",
        "end_time": null
      },
      "exam_overview": {
        "exam_overview_id": 1,
        "exam": "ICSO",
        "grade": 5,
        "level": 1,
        "total_questions": 50,
        "total_marks": 50,
        "total_time_mins": 60
      },
      "section": {
        "section_id": 1,
        "section": "Computer Basics"
      }
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "page_size": 10,
    "total_pages": 1,
    "has_next": false,
    "has_previous": false
  },
  "statistics": {
    "total_time": 1800,
    "best_score": 88.5,
    "average_score": 75.3,
    "total_attempts": 10
  }
}
```

**Error Responses**:

- `500`: Failed to retrieve user practice section exams

---

### 11. Practice Exam Attempt Details APIs

#### 11.1 Update Practice Exam Attempt Details

**Endpoint**: `PUT /practice_exam_attempt_details/{practice_exam_attempt_details_id}`

**Description**: Update or append question-answer details for a practice exam attempt. If a question already exists, it updates the status and selected answer. Otherwise, it appends a new entry.

**Path Parameters**:

- `practice_exam_attempt_details_id` (integer): ID of the practice exam attempt

**Request Body**:

```json
{
  "question_no": 1,
  "question_id": 1,
  "status": 1,
  "selected_answer": "B"
}
```

**Status Values**:

- `0`: Not answered
- `1`: Answered
- `2`: Marked for review

**Response** (200 OK):

```json
{
  "practice_exam_attempt_details_id": 1,
  "user_practice_exam_id": 1,
  "que_ans_details": [
    {
      "question_no": 1,
      "question_id": 1,
      "status": 1,
      "selected_answer": "B"
    }
  ],
  "score": 0,
  "total_time": 0,
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": null
}
```

**Error Responses**:

- `400`: question_id is required
- `400`: status is required
- `400`: Invalid data format
- `404`: Practice exam attempt details not found
- `500`: Database error occurred

---

#### 11.2 Get Practice Exam Attempt Details

**Endpoint**: `GET /practice_exam_attempt_details/{practice_exam_attempt_details_id}`

**Description**: Get question-answer details for a specific practice exam attempt

**Path Parameters**:

- `practice_exam_attempt_details_id` (integer): ID of the practice exam attempt

**Response** (200 OK):

```json
[
  {
    "question_no": 1,
    "question_id": 1,
    "status": 1,
    "selected_answer": "B"
  },
  {
    "question_no": 2,
    "question_id": 2,
    "status": 0,
    "selected_answer": null
  }
]
```

**Error Responses**:

- `404`: Practice exam attempt details not found
- `500`: Failed to retrieve practice exam attempt details

---

#### 11.3 Finish Practice Exam Attempt

**Endpoint**: `PUT /practice_exam_attempt_details_finish/{practice_exam_attempt_details_id}`

**Description**: Update score, total_time, and end_time for a practice exam attempt when the exam is finished

**Path Parameters**:

- `practice_exam_attempt_details_id` (integer): ID of the practice exam attempt

**Request Body**:

```json
{
  "score": 8,
  "total_time": 1800,
  "end_time": "2024-01-15T11:00:00Z"
}
```

**Response** (200 OK):

```json
{
  "practice_exam_attempt_details_id": 1,
  "user_practice_exam_id": 1,
  "que_ans_details": [
    {
      "question_no": 1,
      "question_id": 1,
      "status": 1,
      "selected_answer": "B"
    }
  ],
  "score": 8,
  "total_time": 1800,
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T11:00:00Z",
  "user_practice_exam": {
    "user_practice_exam_id": 1,
    "user_id": 1,
    "exam_overview_id": 1,
    "section_id": 1,
    "syllabus_id": 1,
    "difficulty": "easy",
    "attempt_count": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses**:

- `404`: Practice exam attempt details not found
- `500`: Failed to update practice exam attempt details

---

## 📋 Request/Response Models

### Common Models

#### ExamResponse

```json
{
  "exam_overview_id": 1,
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "total_questions": 50,
  "total_marks": 50,
  "total_time_mins": 60
}
```

#### UserResponse

```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "date_of_birth": "2005-01-15",
  "country_code": "+91",
  "phone_number": "9876543210",
  "profile_image": "https://example.com/profile.jpg",
  "school_name": "ABC High School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "email_verified": false,
  "phone_verified": false,
  "last_login": "2024-01-15T10:30:00Z",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### QuestionResponse

```json
{
  "question_id": 1,
  "syllabus_id": 1,
  "difficulty": "easy",
  "question_text": "Which of the following is an input device?",
  "option_a": "Monitor",
  "option_b": "Keyboard",
  "option_c": "Speaker",
  "option_d": "Printer",
  "correct_option": "B",
  "solution": "Keyboard is an input device.",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "question_image_url": null,
  "option_a_image_url": null,
  "option_b_image_url": null,
  "option_c_image_url": null,
  "option_d_image_url": null
}
```

---

## ⚠️ Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request data or validation error
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Account deactivated or insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Database connection error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

1. **Email Already Registered** (400)

   ```json
   {
     "detail": "Email already registered"
   }
   ```

2. **Invalid Credentials** (401)

   ```json
   {
     "detail": "Invalid email or password"
   }
   ```

3. **Resource Not Found** (404)

   ```json
   {
     "detail": "Exam not found"
   }
   ```

4. **Validation Error** (400)
   ```json
   {
     "detail": "Database constraint violation: total_marks must equal no_of_questions × marks_per_question"
   }
   ```

---

## 🌐 CORS Configuration

The API is configured to allow cross-origin requests from:

- `http://localhost:3000` (Next.js default)
- `http://localhost:3001` (Alternative frontend port)
- `https://olympiad-app-backend.onrender.com` (Production backend)
- `*` (All origins - for development only)

**Important**: In production, restrict `allow_origins` to specific frontend URLs only.

---

## 📊 Data Flow

Understanding the data hierarchy:

```
Exam Overview
    ├── Sections
    │   └── Syllabus (Topics/Subtopics)
    │       └── Questions
    └── Notes

Users
    ├── User Exams (Assigned Exams)
    └── User Practice Exams
        └── Practice Exam Attempt Details
            └── Question-Answer Details
```

**Key Relationships**:

1. Each **Exam** can have multiple **Sections**
2. Each **Section** can have multiple **Syllabus Topics**
3. Each **Syllabus Topic** can have multiple **Questions**
4. Each **Exam** can have multiple **Notes**
5. Each **User** can have multiple **User Exams**
6. Each **User** can have multiple **Practice Exams**
7. Each **Practice Exam** has one **Practice Exam Attempt Details** record

**Cascade Deletes**:

- Deleting an exam deletes all sections, syllabus, questions, and notes
- Deleting a section deletes all syllabus and questions for that section
- Deleting a syllabus topic deletes all questions for that topic

---

## 🐛 Troubleshooting

### Issue: "Email already registered"

**Cause**: Trying to register with an email that already exists.

**Solution**: Use a different email or login with existing credentials.

---

### Issue: "CORS error" or "No 'Access-Control-Allow-Origin' header"

**Cause**: Frontend origin not allowed in CORS configuration.

**Solution**:

1. Check if your frontend URL is in the `allow_origins` list in `main.py`
2. Restart the FastAPI server after making changes

---

### Issue: "405 Method Not Allowed" on preflight request

**Cause**: CORS middleware not properly configured.

**Solution**: Ensure CORS middleware is added in `main.py` (already configured).

---

### Issue: "Database connection error"

**Cause**: PostgreSQL is not running or wrong credentials in `.env`.

**Solution**:

1. Check if PostgreSQL service is running
2. Verify credentials in `.env` file
3. Test database connection manually

---

### Issue: "Foreign key constraint violation"

**Cause**: Trying to create a record with a parent that doesn't exist.

**Solution**:

- For sections: Make sure the exam exists first
- For syllabus: Make sure both exam and section exist
- For questions: Make sure the syllabus topic exists
- For notes: Make sure the exam exists
- For user exams: Make sure both user and exam exist

---

### Issue: "violates check constraint sections_total_marks_ck"

**Cause**: `total_marks` doesn't match `no_of_questions × marks_per_question`.

**Solution**: Calculate correctly: `total_marks = no_of_questions × marks_per_question`

**Example:**

- 10 questions × 1 mark = 10 total marks ✅
- 20 questions × 2 marks = 40 total marks ✅
- 10 questions × 1 mark = 5 total marks ❌

---

### Issue: "duplicate key value violates unique constraint"

**Cause**: Database sequence is out of sync or trying to create duplicate record.

**Solution**:

1. For sequences: Run sequence fix SQL queries
2. For duplicates: Check if record already exists before creating

---

### Issue: Module import errors

**Cause**: Missing `__init__.py` in routers folder or virtual environment not activated.

**Solution**:

1. Ensure `routers/__init__.py` exists
2. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)

---

## ✅ Best Practices

1. **Always use filters when querying questions** to avoid loading too many records
2. **Check parent existence** before creating child records
3. **Use the analytics endpoint** to get statistics before generating questions
4. **Use the full overview endpoint** sparingly as it returns large datasets
5. **Implement pagination** for large result sets (already implemented for practice exams)
6. **Handle errors gracefully** on the frontend
7. **Validate data** on both frontend and backend
8. **Use HTTPS** in production
9. **Restrict CORS origins** in production
10. **Add authentication middleware** before deploying to production
11. **Use environment variables** for sensitive data (database credentials, API keys)
12. **Test all endpoints** before deploying
13. **Monitor API performance** and optimize slow queries
14. **Keep dependencies updated** for security patches

---

## 📝 Notes

- All timestamps are in UTC format (ISO 8601)
- Question difficulty values: `easy`, `medium`, `hard`
- Question status values: `0` (not answered), `1` (answered), `2` (marked for review)
- Practice exam section endpoint only returns records where `syllabus_id = 0` AND `difficulty = ''`
- Practice exam topic endpoint excludes records where `syllabus_id = 0` OR `difficulty = ''`
- Questions for section endpoint randomly selects questions based on `no_of_questions_section`

---

## 🔐 Security Considerations

⚠️ **Important**: This API currently does not implement authentication/authorization middleware. Before deploying to production:

1. **Add JWT authentication** or similar authentication mechanism
2. **Implement role-based access control** (RBAC)
3. **Hash passwords** (currently stored as plain text)
4. **Add rate limiting** to prevent abuse
5. **Use HTTPS** for all communications
6. **Sanitize user inputs** to prevent SQL injection (already handled by parameterized queries)
7. **Validate file uploads** if implementing file upload features
8. **Implement CSRF protection** for state-changing operations

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

Olympiad App Development Team

---

## 🙏 Acknowledgments

- FastAPI documentation
- PostgreSQL documentation
- Python community
- Pydantic documentation

---

## 📞 Support

For issues, questions, or contributions, please contact the development team or create an issue in the repository.

---

**Last Updated**: January 2024

**API Version**: 1.0.0
