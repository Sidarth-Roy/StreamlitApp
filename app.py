import streamlit as st
from PIL import Image
import pytesseract
import snowflake.connector
from google.cloud import firestore
import io

# Function to extract text using pytesseract (OCR)
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to extract key information from the resume
def extract_resume_keywords(text):
    # Example logic to extract basic resume info (customize based on your needs)
    name = "Not Found"
    email = "Not Found"
    skills = []
    
    # Example keyword extraction (you can enhance this with regex or NLP)
    lines = text.splitlines()
    for line in lines:
        if "@" in line and "." in line:  # Basic email detection
            email = line.strip()
        if "Python" in line or "Java" in line or "SQL" in line:
            skills.append(line.strip())
    
    return {
        "name": name,  # Add logic for extracting name
        "email": email,
        "skills": skills
    }

# Function to store extracted data in Snowflake
def store_in_snowflake(resume_data):
    # Snowflake connection (use your own Snowflake credentials)
    conn = snowflake.connector.connect(
        user='YOUR_SNOWFLAKE_USER',
        password='YOUR_SNOWFLAKE_PASSWORD',
        account='YOUR_SNOWFLAKE_ACCOUNT'
    )
    
    cs = conn.cursor()
    try:
        cs.execute("USE DATABASE your_database")
        cs.execute("USE SCHEMA your_schema")

        # Insert data into a Snowflake table
        insert_query = """
        INSERT INTO resumes (name, email, skills) 
        VALUES (%s, %s, %s)
        """
        cs.execute(insert_query, (resume_data["name"], resume_data["email"], ", ".join(resume_data["skills"])))

    finally:
        cs.close()
        conn.close()

# Function to upload the file/image to Firestore
def upload_to_firestore(file_name, file_content):
    # Initialize Firestore client (ensure your Firestore project is set up and authenticated)
    db = firestore.Client()
    
    # Store the file in Firestore (as bytes)
    doc_ref = db.collection('resumes').document(file_name)
    doc_ref.set({
        "file_name": file_name,
        "file_content": file_content
    })

# Main function for handling file upload and camera input
def upload_file():
    st.title("Upload Data: File or Camera")
    
    # Upload a file (limit up to 10 MB)
    uploaded_file = st.file_uploader("Choose a file (Max size: 10MB)", type=["jpg", "jpeg", "pdf", "txt", "docx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("File size exceeds 10 MB!")
        else:
            # Process and extract text from the uploaded image or file
            if uploaded_file.type in ["image/jpg", "image/jpeg", "application/pdf"]:
                image = Image.open(uploaded_file)
                extracted_text = extract_text_from_image(image)
                resume_data = extract_resume_keywords(extracted_text)
                
                st.write("Extracted Resume Data:", resume_data)
                
                # Store data in Snowflake
                store_in_snowflake(resume_data)
                
                # Upload file to Firestore
                file_content = uploaded_file.getvalue()
                upload_to_firestore(uploaded_file.name, file_content)

                st.success("Resume data stored in Snowflake and file uploaded to Firestore!")
    
    # Camera input
    use_camera = st.checkbox("Would you like to capture a picture using your camera?")
    
    if use_camera:
        img_file_buffer = st.camera_input("Capture a picture")
        if img_file_buffer is not None:
            image = Image.open(img_file_buffer)
            extracted_text = extract_text_from_image(image)
            resume_data = extract_resume_keywords(extracted_text)
            
            st.write("Extracted Resume Data:", resume_data)
            
            # Store data in Snowflake
            store_in_snowflake(resume_data)
            
            # Upload captured image to Firestore
            img_bytes = img_file_buffer.getvalue()
            upload_to_firestore("captured_image.jpg", img_bytes)
            
            st.success("Resume data stored in Snowflake and image uploaded to Firestore!")

# Placeholder function for Chatbot
def chatbot_page():
    st.title("Chatbot Page")
    st.write("This is where your chatbot will go. Customize it with your chatbot functionality!")

# Placeholder function for Dashboard
def dashboard_page():
    st.title("Dashboard")
    st.write("This is where your data dashboard will go. Customize it with your analytics and visualizations!")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Data", "Chatbot", "Dashboard"])

# Render selected page
if page == "Upload Data":
    upload_file()
elif page == "Chatbot":
    chatbot_page()
elif page == "Dashboard":
    dashboard_page()
