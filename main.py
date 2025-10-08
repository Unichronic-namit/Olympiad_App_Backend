from fastapi import FastAPI
from routers import exam_overview, sections, syllabus, notes, questions, analytics, auth

app = FastAPI(title="Olympiad App API", version="1.0.0")

# Include routers
app.include_router(exam_overview.router)
app.include_router(sections.router)
app.include_router(syllabus.router)
app.include_router(notes.router)
app.include_router(questions.router)
app.include_router(analytics.router)
app.include_router(auth.router)

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