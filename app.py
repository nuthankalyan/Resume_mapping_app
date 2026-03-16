import streamlit as st
import os
import re
from pypdf import PdfReader

# Page configuration
st.set_page_config(
    page_title="Resume Skill Extractor",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stTitle {
            text-align: center;
            margin-bottom: 1rem;
        }
        .upload-section {
            background-color: #f8f9fa;
            padding: 4rem 2rem;
            border-radius: 12px;
            margin: 3rem 0;
            border: 2px dashed #e0e0e0;
            text-align: center;
        }
        .stFileUploader {
            margin: 2rem 0;
        }
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1.5rem;
        }
        .skill-badge {
            background-color: #e3f2fd;
            border: 1px solid #2196f3;
            color: #1976d2;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

# List of common skills to extract
COMMON_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'golang', 'swift', 'kotlin',
    'r', 'matlab', 'scala', 'rust', 'typescript', 'perl', 'objective-c', 'dart', 'groovy',
    
    # Web Development
    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
    'spring', 'asp.net', 'fastapi', 'nextjs', 'svelte', 'webpack', 'jquery',
    
    # Data & Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
    'dynamodb', 'firebase', 'oracle', 'sqlite', 'hadoop', 'spark', 'hive',
    
    # Data Science & ML
    'machine learning', 'deep learning', 'tensorflow', 'keras', 'pytorch', 'scikit-learn',
    'pandas', 'numpy', 'matplotlib', 'seaborn', 'nlp', 'computer vision', 'cv',
    'data analysis', 'statistical analysis', 'data visualization',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
    'git', 'github', 'gitlab', 'ci/cd', 'devops', 'cloud computing', 'microservices',
    
    # Other Tools & Frameworks
    'rest api', 'graphql', 'soap', 'linux', 'windows', 'macos', 'agile', 'scrum',
    'jira', 'confluence', 'slack', 'vim', 'vs code', 'visual studio', 'eclipse',
    'figma', 'photoshop', 'illustrator', 'blender'
}

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_skills(resume_text):
    """Extract skills from resume text"""
    # Convert to lowercase for matching
    resume_lower = resume_text.lower()
    
    found_skills = set()
    
    # Search for each skill in the resume
    for skill in COMMON_SKILLS:
        # Use word boundaries to match whole words/phrases
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_lower):
            found_skills.add(skill.title())
    
    # Sort skills alphabetically
    return sorted(found_skills)

# Title and description
st.title("📄 Resume Skill Extractor")
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1em;'>Upload your resume to extract key skills</p>", unsafe_allow_html=True)

st.markdown("")  # Space
st.markdown("")  # Space

# Create upload section with better spacing

# Create centered upload area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        label="Choose a PDF file",
        type="pdf",
        help="Upload a PDF resume to extract skills",
        label_visibility="collapsed"
    )

st.markdown("")  # Space
st.markdown("")  # Space

# Display uploaded file information and extract skills
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")
    
    st.markdown("")  # Space
    
    # File metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="File Name", value=uploaded_file.name)
    
    with col2:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.metric(label="File Size", value=f"{file_size_mb:.2f} MB")
    
    st.markdown("")  # Space
    st.markdown("---")
    st.markdown("")  # Space
    
    # Extract and display skills
    st.subheader("🎯 Extracted Skills")
    
    with st.spinner("Analyzing resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            extracted_skills = extract_skills(resume_text)
            
            if extracted_skills:
                # Display skills in a formatted way
                st.markdown(f"**Found {len(extracted_skills)} skills:**")
                
                # Create skill badges
                skills_html = '<div class="skills-container">'
                for skill in extracted_skills:
                    skills_html += f'<span class="skill-badge">{skill}</span>'
                skills_html += '</div>'
                
                st.markdown(skills_html, unsafe_allow_html=True)
                
                st.markdown("")  # Space
                
                # Display skills as a list as well
                with st.expander("📋 View as List"):
                    for i, skill in enumerate(extracted_skills, 1):
                        st.write(f"{i}. {skill}")
            else:
                st.warning("⚠️ No skills found in the resume. Please check the file.")
        else:
            st.error("Could not extract text from PDF.")
    
    st.markdown("")  # Space
    st.markdown("---")
    st.markdown("")  # Space
    
    # Save file option
    if st.button("💾 Save Resume", use_container_width=True):
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ Resume saved to `uploads/{uploaded_file.name}`")
else:
    st.info("📌 Upload your resume in PDF format to get started")

st.markdown("")  # Space
st.markdown("")  # Space
st.markdown("<p style='text-align: center; color: #999; font-size: 0.85em;'>Supported format: PDF | Secure & Private</p>", unsafe_allow_html=True)
