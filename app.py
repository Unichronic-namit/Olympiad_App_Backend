import streamlit as st
import requests

# API Base URL
API_BASE_URL = "https://olympiad-app-backend.onrender.com"

st.title("Olympiad API Tester")

# Sidebar for selecting module
st.sidebar.header("Select Module")
module = st.sidebar.selectbox(
    "Choose API Module",
    ["Exams", "Sections", "Syllabus", "Notes", "Questions", "Analytics", "Auth"]
)

# ----- EXAMS MODULE -----
if module == "Exams":
    st.header("Exam Overview APIs")
    
    action = st.radio("Select Action", ["Get All Exams", "Get Single Exam", "Create Exam", "Update Exam", "Delete Exam"])
    
    if action == "Get All Exams":
        if st.button("Fetch All Exams"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/exams")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Get Single Exam":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        if st.button("Fetch Exam"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/exams/{exam_id}")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Create Exam":
        exam = st.text_input("Exam Name")
        grade = st.number_input("Grade", min_value=1, max_value=12, step=1)
        level = st.number_input("Level", min_value=1, step=1)
        total_questions = st.number_input("Total Questions", min_value=0, step=1)
        total_marks = st.number_input("Total Marks", min_value=0, step=1)
        total_time_mins = st.number_input("Total Time (mins)", min_value=1, step=1)
        
        if st.button("Create Exam"):
            with st.spinner("Creating..."):
                data = {
                    "exam": exam,
                    "grade": grade,
                    "level": level,
                    "total_questions": total_questions,
                    "total_marks": total_marks,
                    "total_time_mins": total_time_mins
                }
                response = requests.post(f"{API_BASE_URL}/exams", json=data)
                if response.status_code == 201:
                    st.success("Exam created!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Update Exam":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        total_marks = st.number_input("Total Marks", min_value=0, step=1)
        total_time_mins = st.number_input("Total Time (mins)", min_value=1, step=1)
        
        if st.button("Update Exam"):
            with st.spinner("Updating..."):
                data = {
                    "total_marks": total_marks,
                    "total_time_mins": total_time_mins
                }
                response = requests.put(f"{API_BASE_URL}/exams/{exam_id}", json=data)
                if response.status_code == 200:
                    st.success("Exam updated!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Delete Exam":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        if st.button("Delete Exam"):
            with st.spinner("Deleting..."):
                response = requests.delete(f"{API_BASE_URL}/exams/{exam_id}")
                if response.status_code == 204:
                    st.success("Exam deleted!")
                else:
                    st.error(f"Error: {response.status_code}")

# ----- SECTIONS MODULE -----
elif module == "Sections":
    st.header("Sections APIs")
    
    action = st.radio("Select Action", ["Get All Sections", "Create Section", "Update Section", "Delete Section"])
    
    if action == "Get All Sections":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        if st.button("Fetch Sections"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/exams/{exam_id}/sections")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Create Section":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        section = st.text_input("Section Name")
        no_of_questions = st.number_input("Number of Questions", min_value=1, step=1)
        marks_per_question = st.number_input("Marks per Question", min_value=1, step=1)
        total_marks = st.number_input("Total Marks", min_value=1, step=1)
        
        if st.button("Create Section"):
            with st.spinner("Creating..."):
                data = {
                    "section": section,
                    "no_of_questions": no_of_questions,
                    "marks_per_question": marks_per_question,
                    "total_marks": total_marks
                }
                response = requests.post(f"{API_BASE_URL}/exams/{exam_id}/sections", json=data)
                if response.status_code == 201:
                    st.success("Section created!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Update Section":
        section_id = st.number_input("Section ID", min_value=1, step=1)
        no_of_questions = st.number_input("Number of Questions", min_value=1, step=1)
        total_marks = st.number_input("Total Marks", min_value=1, step=1)
        
        if st.button("Update Section"):
            with st.spinner("Updating..."):
                data = {
                    "no_of_questions": no_of_questions,
                    "total_marks": total_marks
                }
                response = requests.put(f"{API_BASE_URL}/sections/{section_id}", json=data)
                if response.status_code == 200:
                    st.success("Section updated!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Delete Section":
        section_id = st.number_input("Section ID", min_value=1, step=1)
        if st.button("Delete Section"):
            with st.spinner("Deleting..."):
                response = requests.delete(f"{API_BASE_URL}/sections/{section_id}")
                if response.status_code == 204:
                    st.success("Section deleted!")
                else:
                    st.error(f"Error: {response.status_code}")

# ----- SYLLABUS MODULE -----
elif module == "Syllabus":
    st.header("Syllabus APIs")
    
    action = st.radio("Select Action", ["Get Syllabus", "Create Topic", "Update Topic", "Delete Topic"])
    
    if action == "Get Syllabus":
        section_id = st.number_input("Section ID", min_value=1, step=1)
        if st.button("Fetch Syllabus"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/sections/{section_id}/syllabus")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Create Topic":
        section_id = st.number_input("Section ID", min_value=1, step=1)
        topic = st.text_input("Topic")
        subtopic = st.text_input("Subtopic (optional)")
        
        if st.button("Create Topic"):
            with st.spinner("Creating..."):
                data = {
                    "topic": topic,
                    "subtopic": subtopic
                }
                response = requests.post(f"{API_BASE_URL}/sections/{section_id}/syllabus", json=data)
                if response.status_code == 201:
                    st.success("Topic created!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Update Topic":
        syllabus_id = st.number_input("Syllabus ID", min_value=1, step=1)
        topic = st.text_input("Topic")
        subtopic = st.text_input("Subtopic")
        
        if st.button("Update Topic"):
            with st.spinner("Updating..."):
                data = {
                    "topic": topic,
                    "subtopic": subtopic
                }
                response = requests.put(f"{API_BASE_URL}/syllabus/{syllabus_id}", json=data)
                if response.status_code == 200:
                    st.success("Topic updated!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Delete Topic":
        syllabus_id = st.number_input("Syllabus ID", min_value=1, step=1)
        if st.button("Delete Topic"):
            with st.spinner("Deleting..."):
                response = requests.delete(f"{API_BASE_URL}/syllabus/{syllabus_id}")
                if response.status_code == 204:
                    st.success("Topic deleted!")
                else:
                    st.error(f"Error: {response.status_code}")

# ----- NOTES MODULE -----
elif module == "Notes":
    st.header("Notes APIs")
    
    action = st.radio("Select Action", ["Get All Notes", "Create Note", "Update Note", "Delete Note"])
    
    if action == "Get All Notes":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        if st.button("Fetch Notes"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/exams/{exam_id}/notes")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Create Note":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        note = st.text_area("Note")
        
        if st.button("Create Note"):
            with st.spinner("Creating..."):
                data = {"note": note}
                response = requests.post(f"{API_BASE_URL}/exams/{exam_id}/notes", json=data)
                if response.status_code == 201:
                    st.success("Note created!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Update Note":
        note_id = st.number_input("Note ID", min_value=1, step=1)
        note = st.text_area("Note")
        
        if st.button("Update Note"):
            with st.spinner("Updating..."):
                data = {"note": note}
                response = requests.put(f"{API_BASE_URL}/notes/{note_id}", json=data)
                if response.status_code == 200:
                    st.success("Note updated!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Delete Note":
        note_id = st.number_input("Note ID", min_value=1, step=1)
        if st.button("Delete Note"):
            with st.spinner("Deleting..."):
                response = requests.delete(f"{API_BASE_URL}/notes/{note_id}")
                if response.status_code == 204:
                    st.success("Note deleted!")
                else:
                    st.error(f"Error: {response.status_code}")

# ----- QUESTIONS MODULE -----
elif module == "Questions":
    st.header("Questions APIs")
    
    action = st.radio("Select Action", ["Get All Questions", "Get Questions by Topic", "Add Question", "Update Question", "Delete Question"])
    
    if action == "Get All Questions":
        syllabus_id = st.number_input("Syllabus ID (optional)", min_value=1, step=1, value=1)
        difficulty = st.text_input("Difficulty (optional, e.g., easy, medium, hard)")
        
        if st.button("Fetch Questions"):
            with st.spinner("Loading..."):
                params = {}
                if syllabus_id > 0:
                    params['syllabus_id'] = syllabus_id
                if difficulty:
                    params['difficulty'] = difficulty
                
                response = requests.get(f"{API_BASE_URL}/questions", params=params)
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Get Questions by Topic":
        syllabus_id = st.number_input("Syllabus ID", min_value=1, step=1)
        
        if st.button("Fetch Questions"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/syllabus/{syllabus_id}/questions")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Add Question":
        syllabus_id = st.number_input("Syllabus ID", min_value=1, step=1)
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        question_text = st.text_area("Question Text")
        option_a = st.text_input("Option A")
        option_b = st.text_input("Option B")
        option_c = st.text_input("Option C")
        option_d = st.text_input("Option D")
        correct_option = st.selectbox("Correct Option", ["A", "B", "C", "D"])
        solution = st.text_area("Solution (optional)")
        
        if st.button("Add Question"):
            with st.spinner("Creating..."):
                data = {
                    "difficulty": difficulty,
                    "question_text": question_text,
                    "option_a": option_a,
                    "option_b": option_b,
                    "option_c": option_c,
                    "option_d": option_d,
                    "correct_option": correct_option,
                    "solution": solution
                }
                response = requests.post(f"{API_BASE_URL}/syllabus/{syllabus_id}/questions", json=data)
                if response.status_code == 201:
                    st.success("Question added!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Update Question":
        question_id = st.number_input("Question ID", min_value=1, step=1)
        solution = st.text_area("New Solution")
        
        if st.button("Update Question"):
            with st.spinner("Updating..."):
                data = {"solution": solution}
                response = requests.put(f"{API_BASE_URL}/questions/{question_id}", json=data)
                if response.status_code == 200:
                    st.success("Question updated!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Delete Question":
        question_id = st.number_input("Question ID", min_value=1, step=1)
        
        if st.button("Delete Question"):
            with st.spinner("Deleting..."):
                response = requests.delete(f"{API_BASE_URL}/questions/{question_id}")
                if response.status_code == 204:
                    st.success("Question deleted!")
                else:
                    st.error(f"Error: {response.status_code}")

# ----- ANALYTICS MODULE -----
elif module == "Analytics":
    st.header("Combined & Analytics APIs")
    
    action = st.radio("Select Action", ["Get Full Exam Overview", "Get Exam Analytics"])
    
    if action == "Get Full Exam Overview":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        
        if st.button("Fetch Full Overview"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/exams/{exam_id}/overview")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Get Exam Analytics":
        exam_id = st.number_input("Exam_overview ID", min_value=1, step=1)
        
        if st.button("Fetch Analytics"):
            with st.spinner("Loading..."):
                response = requests.get(f"{API_BASE_URL}/analytics/exam/{exam_id}")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")

# ----- AUTH MODULE -----
elif module == "Auth":
    st.header("Authentication APIs")
    
    action = st.radio("Select Action", ["Signup", "Login"])
    
    if action == "Signup":
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        grade = st.number_input("Grade", min_value=1, max_value=12, step=1)
        dob = st.date_input("Date of Birth")
        country_code = st.text_input("Country Code (e.g., +91)")
        phone_number = st.text_input("Phone Number")
        profile_image = st.text_input("Profile Image URL")
        school_name = st.text_input("School Name")
        city = st.text_input("City")
        state = st.text_input("State")
        
        if st.button("Signup"):
            with st.spinner("Creating account..."):
                data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "grade": grade,
                    "date_of_birth": str(dob),
                    "country_code": country_code,
                    "phone_number": phone_number,
                    "profile_image": profile_image,
                    "school_name": school_name,
                    "city": city,
                    "state": state
                }
                response = requests.post(f"{API_BASE_URL}/signup", json=data)
                if response.status_code == 201:
                    st.success("Account created!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")
    
    elif action == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            with st.spinner("Logging in..."):
                data = {
                    "email": email,
                    "password": password
                }
                response = requests.post(f"{API_BASE_URL}/login", json=data)
                if response.status_code == 200:
                    st.success("Login successful!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}")