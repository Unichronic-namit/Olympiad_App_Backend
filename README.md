# 🏆 Olympiad App - Backend API

A comprehensive FastAPI-based REST API for managing olympiad exams, sections, syllabus, questions, notes, and analytics.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Exam Management**: Create, read, update, and delete exam overviews
- **Section Management**: Manage exam sections with questions and marks
- **Syllabus Management**: Organize topics and subtopics for each section
- **Question Bank**: Store and manage MCQ questions linked to syllabus topics
- **Notes Management**: Add study material and notes for exams
- **Combined Endpoints**: Get complete exam structure in one call
- **Analytics**: Get statistics on topics and questions by difficulty
- **Search**: Search questions across the entire question bank
- **Data Validation**: Automatic validation using Pydantic models
- **Error Handling**: Comprehensive error messages for debugging
- **Auto-generated API Docs**: Interactive Swagger UI and ReDoc

## 🛠 Tech Stack

- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.30.6
- **Database**: PostgreSQL
- **Database Driver**: psycopg2-binary 2.9.10
- **Validation**: Pydantic 2.9.2
- **Environment**: python-dotenv

## 📁 Project Structure

```
olympiad_app/
├── .env                    # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── main.py               # Application entry point
├── database.py           # Database connection
├── models.py             # Pydantic models
└── routers/
    ├── __init__.py       # Router initialization
    ├── exam_overview.py  # Exam endpoints
    ├── sections.py       # Section endpoints
    ├── syllabus.py       # Syllabus endpoints
    ├── questions.py      # Question endpoints
    ├── notes.py          # Notes endpoints
    └── analytics.py      # Combined & Analytics endpoints
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
   cd olympiad_app
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
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your database credentials**:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=olympiad_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

## 🗄️ Database Setup

### 1. Create Database

```sql
CREATE DATABASE olympiad_db;
```

### 2. Create Tables

```sql
-- Exam Overview Table
CREATE TABLE IF NOT EXISTS exam_overview (
  exam_overview_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  exam              VARCHAR(100) NOT NULL,
  grade             SMALLINT     NOT NULL CHECK (grade BETWEEN 1 AND 12),
  level             SMALLINT     NOT NULL,
  total_questions   INTEGER      NOT NULL CHECK (total_questions >= 0),
  total_marks       INTEGER      NOT NULL CHECK (total_marks >= 0),
  total_time_mins   INTEGER      NOT NULL CHECK (total_time_mins > 0),
  CONSTRAINT exam_overview_uk UNIQUE (exam, grade, level)
);

-- Sections Table
CREATE TABLE IF NOT EXISTS sections (
  section_id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  exam_overview_id   INTEGER      NOT NULL,
  section            VARCHAR(100) NOT NULL,
  no_of_questions    INTEGER      NOT NULL CHECK (no_of_questions > 0),
  marks_per_question INTEGER      NOT NULL CHECK (marks_per_question > 0),
  total_marks        INTEGER      NOT NULL,
  CONSTRAINT sections_exam_fk
    FOREIGN KEY (exam_overview_id) REFERENCES exam_overview(exam_overview_id)
    ON DELETE CASCADE,
  CONSTRAINT sections_total_marks_ck
    CHECK (total_marks = no_of_questions * marks_per_question),
  CONSTRAINT sections_uk UNIQUE (exam_overview_id, section)
);

-- Syllabus Table
CREATE TABLE IF NOT EXISTS syllabus (
  syllabus_id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  exam_overview_id INTEGER      NOT NULL,
  section_id       INTEGER      NOT NULL,
  topic            VARCHAR(200) NOT NULL,
  subtopic         VARCHAR(200) DEFAULT '',
  CONSTRAINT syllabus_exam_fk
    FOREIGN KEY (exam_overview_id) REFERENCES exam_overview(exam_overview_id)
    ON DELETE CASCADE,
  CONSTRAINT syllabus_section_fk
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
    ON DELETE CASCADE,
  CONSTRAINT syllabus_uk UNIQUE (exam_overview_id, section_id, topic, subtopic)
);

-- Questions Table
CREATE TABLE IF NOT EXISTS questions (
  question_id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  syllabus_id     INTEGER     NOT NULL,
  difficulty      VARCHAR(20) NOT NULL,
  question_text   TEXT        NOT NULL,
  option_a        TEXT        NOT NULL,
  option_b        TEXT        NOT NULL,
  option_c        TEXT        NOT NULL,
  option_d        TEXT        NOT NULL,
  correct_option  VARCHAR(5)  NOT NULL,
  solution        TEXT        NOT NULL DEFAULT '',
  is_active       BOOLEAN     NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT questions_syllabus_fk
    FOREIGN KEY (syllabus_id) REFERENCES syllabus(syllabus_id)
    ON DELETE CASCADE
);

-- Notes Table
CREATE TABLE IF NOT EXISTS notes (
  note_id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  note             TEXT    NOT NULL,
  exam_overview_id INTEGER NOT NULL,
  CONSTRAINT notes_exam_fk
    FOREIGN KEY (exam_overview_id) REFERENCES exam_overview(exam_overview_id)
    ON DELETE CASCADE
);
```

### 3. Fix Sequences (if needed)

If you encounter primary key conflicts, run:

```sql
-- Fix all sequences at once
SELECT setval('exam_overview_exam_overview_id_seq', 
              (SELECT COALESCE(MAX(exam_overview_id), 0) FROM exam_overview), true);

SELECT setval('sections_section_id_seq', 
              (SELECT COALESCE(MAX(section_id), 0) FROM sections), true);

SELECT setval('syllabus_syllabus_id_seq', 
              (SELECT COALESCE(MAX(syllabus_id), 0) FROM syllabus), true);

SELECT setval('questions_question_id_seq', 
              (SELECT COALESCE(MAX(question_id), 0) FROM questions), true);

SELECT setval('notes_note_id_seq', 
              (SELECT COALESCE(MAX(note_id), 0) FROM notes), true);
```

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

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### 📘 Exam Overview Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exams` | Get all exams |
| GET | `/exams/{exam_overview_id}` | Get exam details |
| POST | `/exams` | Create new exam |
| PUT | `/exams/{exam_overview_id}` | Update exam |
| DELETE | `/exams/{exam_overview_id}` | Delete exam (cascade) |

**Example POST Request:**
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

---

### 📗 Sections Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exams/{exam_overview_id}/sections` | Get all sections for exam |
| POST | `/exams/{exam_overview_id}/sections` | Add new section |
| PUT | `/sections/{section_id}` | Update section |
| DELETE | `/sections/{section_id}` | Delete section (cascade) |

**Example POST Request:**
```json
{
  "section": "Computer Basics",
  "no_of_questions": 10,
  "marks_per_question": 1,
  "total_marks": 10
}
```

**Important**: `total_marks = no_of_questions × marks_per_question`

---

### 📙 Syllabus Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sections/{section_id}/syllabus` | Get syllabus for section |
| POST | `/sections/{section_id}/syllabus` | Add topic/subtopic |
| PUT | `/syllabus/{syllabus_id}` | Update topic/subtopic |
| DELETE | `/syllabus/{syllabus_id}` | Delete topic/subtopic |

**Example POST Request:**
```json
{
  "exam_overview_id": 1,
  "section_id": 1,
  "topic": "Input Devices",
  "subtopic": "Keyboard, Mouse"
}
```

---

### ❓ Questions Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/questions` | Get all questions (with filters) |
| GET | `/syllabus/{syllabus_id}/questions` | Get questions for a topic |
| POST | `/syllabus/{syllabus_id}/questions` | Add new question |
| PUT | `/questions/{question_id}` | Update question/solution |
| DELETE | `/questions/{question_id}` | Delete question |
| POST | `/questions/generate` | Auto generate questions (AI) |
| POST | `/questions/bulk_upload` | Bulk upload from file |

**Example GET with filters:**
```
GET /questions?syllabus_id=22&difficulty=easy
```

**Example POST Request:**
```json
{
  "syllabus_id": 1,
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

**Example AI Generate Request:**
```json
{
  "exam": "ICSO",
  "grade": 5,
  "level": 1,
  "section_id": 1
}
```

---

### 📝 Notes Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exams/{exam_overview_id}/notes` | Get all notes for exam |
| POST | `/exams/{exam_overview_id}/notes` | Add new note |
| PUT | `/notes/{note_id}` | Update note |
| DELETE | `/notes/{note_id}` | Delete note |

**Example POST Request:**
```json
{
  "note": "Revise all input and output devices before mock test."
}
```

---

### 📊 Combined & Analytics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exams/{exam_overview_id}/overview` | Get complete exam structure |
| GET | `/analytics/exam/{exam_overview_id}` | Get exam analytics |
| GET | `/search/questions` | Search in question bank |

**Example Full Overview Response:**
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
      "syllabus": [
        {
          "syllabus_id": 1,
          "topic": "Input Devices",
          "questions": [...]
        }
      ]
    }
  ],
  "notes": [...]
}
```

**Example Analytics Response:**
```json
{
  "exam_overview_id": 1,
  "total_topics": 15,
  "questions_by_difficulty": [
    {"difficulty": "easy", "count": 20},
    {"difficulty": "medium", "count": 18},
    {"difficulty": "hard", "count": 12}
  ]
}
```

**Example Search:**
```
GET /search/questions?q=input device&grade=5
```

## 🐛 Troubleshooting

### Issue: "Exam already exists with this combination"

**Cause**: Trying to create an exam with duplicate (exam, grade, level) combination.

**Solution**: Change the level or grade, or update the existing exam using PUT instead.

### Issue: "duplicate key value violates unique constraint"

**Cause**: Database sequence is out of sync.

**Solution**: Run the sequence fix SQL queries (see Database Setup section 3).

### Issue: "violates check constraint sections_total_marks_ck"

**Cause**: `total_marks` doesn't match `no_of_questions × marks_per_question`.

**Solution**: Calculate correctly: `total_marks = no_of_questions × marks_per_question`

**Example:**
- 10 questions × 1 mark = 10 total marks ✅
- 20 questions × 2 marks = 40 total marks ✅
- 10 questions × 1 mark = 5 total marks ❌

### Issue: Foreign key constraint violation

**Cause**: Trying to create a record with a parent that doesn't exist.

**Solution**: 
- For sections: Make sure the exam exists first
- For syllabus: Make sure both exam and section exist
- For questions: Make sure the syllabus topic exists
- For notes: Make sure the exam exists

### Issue: "Connection refused" or "Database connection error"

**Cause**: PostgreSQL is not running or wrong credentials in `.env`.

**Solution**: 
1. Check if PostgreSQL service is running
2. Verify credentials in `.env` file
3. Test database connection manually

### Issue: Module import errors

**Cause**: Missing `__init__.py` in routers folder.

**Solution**: Create an empty `__init__.py` file in the `routers/` directory:
```bash
# Windows
type nul > routers\__init__.py

# macOS/Linux
touch routers/__init__.py
```

### Issue: "405 Method Not Allowed"

**Cause**: Using wrong endpoint URL.

**Solution**: Check the endpoint structure:
- Sections: `/exams/{id}/sections` (not `/sections`)
- Syllabus: `/sections/{id}/syllabus` (not `/syllabus`)
- Questions: `/syllabus/{id}/questions` (not `/questions/{id}`)
- Notes: `/exams/{id}/notes` (not `/notes`)

## 📝 Data Flow

Understanding the data hierarchy:

```
Exam Overview
    ├── Sections
    │   └── Syllabus (Topics/Subtopics)
    │       └── Questions
    └── Notes
```

**Key Relationships:**
1. Each **Exam** can have multiple **Sections**
2. Each **Section** can have multiple **Syllabus Topics**
3. Each **Syllabus Topic** can have multiple **Questions**
4. Each **Exam** can have multiple **Notes**

**Cascade Deletes:**
- Deleting an exam deletes all sections, syllabus, questions, and notes
- Deleting a section deletes all syllabus and questions for that section
- Deleting a syllabus topic deletes all questions for that topic

## 🔐 Best Practices

1. **Always use filters when querying questions** to avoid loading too many records
2. **Check parent existence** before creating child records
3. **Use the analytics endpoint** to get statistics before generating questions
4. **Use the full overview endpoint** sparingly as it returns large datasets
5. **Implement pagination** for production use (not included in this version)
6. **Add authentication** before deploying to production

## 📊 Future Enhancements

- [ ] AI-powered question generation
- [ ] Bulk upload from CSV/JSON files
- [ ] Question versioning and history
- [ ] User authentication and authorization
- [ ] Question tagging system
- [ ] Advanced search with full-text indexing
- [ ] Export functionality (PDF, Excel)
- [ ] Question difficulty auto-classification
- [ ] Analytics dashboard
- [ ] Pagination for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI documentation
- PostgreSQL documentation
- Python community