from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import exam_overview, sections, syllabus, notes, questions, analytics, auth, user_exams

app = FastAPI(title="Olympiad App API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://olympiad-app-backend.onrender.com",
        "*"  # Allow all origins for development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(exam_overview.router)
app.include_router(sections.router)
app.include_router(syllabus.router)
app.include_router(notes.router)
app.include_router(questions.router)
app.include_router(analytics.router)
app.include_router(auth.router)
app.include_router(user_exams.router)

@app.get("/")
def root():
    return {
        "message": "Olympiad App API",
        "version": "1.0.0",
        "endpoints": {
            "exams": "/exams",
            "sections": "/exams/{exam_overview_id}/sections",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)