import streamlit as st
from PIL import Image

# Function for uploading a file
def upload_file():
    st.title("Upload Data: File or Camera")
    
    # Allow file upload with specific formats and limit the size to 10 MB
    uploaded_file = st.file_uploader("Choose a file (Max size: 10MB)", type=["jpg", "jpeg", "pdf", "txt", "docx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        if uploaded_file.size > 10 * 1024 * 1024:  # 10 MB limit
            st.error("File size exceeds 10 MB!")
        else:
            # Handle image files
            if uploaded_file.type in ["image/jpg", "image/jpeg"]:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
            # Handle PDF files
            elif uploaded_file.type == "application/pdf":
                st.write(f"Uploaded file: {uploaded_file.name} (PDF)")
                st.download_button("Download PDF", uploaded_file, file_name=uploaded_file.name)
            # Handle TXT files
            elif uploaded_file.type == "text/plain":
                text = str(uploaded_file.read(), "utf-8")
                st.text_area("Text File Content", text, height=300)
            # Handle DOCX files
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                st.write(f"Uploaded file: {uploaded_file.name} (DOCX)")
                st.download_button("Download DOCX", uploaded_file, file_name=uploaded_file.name)

    # Ask the user if they want to use the camera
    use_camera = st.checkbox("Would you like to capture a picture using your camera?")
    
    if use_camera:
        img_file_buffer = st.camera_input("Capture a picture")
        if img_file_buffer is not None:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Captured Image", use_column_width=True)

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
