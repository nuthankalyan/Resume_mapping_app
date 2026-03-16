import streamlit as st
import os
import re
from pypdf import PdfReader

# Page configuration
st.set_page_config(
    page_title="Resume Skill Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Root and main container */
        * {
            box-sizing: border-box;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            width: 100%;
            margin: 0;
            padding: 0;
        }
        
        [data-testid="stAppViewContainer"] {
            display: flex;
            justify-content: center;
        }
        
        [data-testid="stMainBlockContainer"] {
            max-width: 1000px;
            width: 100%;
            padding: 2rem 3rem;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Main content area */
        .main {
            width: 100%;
        }
        
        /* Title styling - centered */
        .stTitle h1 {
            text-align: center !important;
            padding: 1rem 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* All headings centered */
        h1, h2, h3, h4, h5, h6 {
            text-align: center !important;
            width: 100% !important;
        }
        
        /* Description text - centered */
        .description-text {
            text-align: center;
            color: #666;
            font-size: 1.1em;
            margin: 1.5rem 0 2.5rem 0;
            line-height: 1.6;
            width: 100%;
        }
        
        /* File uploader - centered with 40% width */
        [data-testid="stFileUploader"] {
            max-width: 40% !important;
            margin: 2rem auto !important;
            width: 40% !important;
        }
        
        [data-testid="stFileUploader"] > div {
            width: 100% !important;
            margin: 0 auto !important;
        }
        
        [data-testid="stFileUploader"] input {
            width: 100% !important;
        }
        
        .stFileUploader {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 2rem auto !important;
        }
        
        .stFileUploader > div {
            width: 40% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
        }
        
        .stFileUploader div {
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Columns centered */
        [data-testid="column"] {
            width: 100% !important;
            margin: 0 auto !important;
        }
        
        /* Metrics - centered layout */
        .stMetric {
            text-align: center;
        }
        
        .stMetric > div {
            justify-content: center;
        }
        
        /* Info/Success/Warning/Error boxes - centered */
        .stAlert {
            margin: 1.5rem auto !important;
            max-width: 100%;
        }
        
        /* Skills container with proper centering */
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 2rem 0;
            justify-content: center;
            width: 100%;
        }
        
        /* Skill badge styling */
        .skill-badge {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 1.5px solid #2196f3;
            color: #1565c0;
            padding: 0.7rem 1.3rem;
            border-radius: 25px;
            font-size: 0.95em;
            font-weight: 500;
            display: inline-block;
            box-shadow: 0 2px 6px rgba(33, 150, 243, 0.2);
            white-space: nowrap;
            transition: all 0.3s ease;
        }
        
        .skill-badge:hover {
            background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
            transform: translateY(-2px);
        }
        
        /* Section headers */
        .section-header {
            text-align: center !important;
            margin: 2.5rem 0 2rem 0 !important;
            font-size: 1.8em !important;
            font-weight: 600 !important;
            color: #333 !important;
            width: 100% !important;
        }
        
        /* Divider styling */
        hr {
            margin: 2rem 0 !important;
            border: none;
            border-top: 1px solid #e0e0e0;
            opacity: 1;
        }
        
        /* Button centering */
        .stButton {
            display: flex;
            justify-content: center;
            width: 100%;
            margin: 2rem 0;
        }
        
        .stButton > button {
            min-width: 300px;
            max-width: 500px;
        }
        
        /* Footer text */
        .footer-text {
            text-align: center;
            color: #999;
            font-size: 0.85em;
            margin-top: 3rem;
            line-height: 1.5;
            width: 100%;
        }
        
        /* Expander - centered */
        .streamlit-expanderHeader {
            text-align: center;
        }
        
        [data-testid="stExpander"] {
            width: 100%;
        }
        
        /* Bold text centering */
        strong {
            display: block;
            text-align: center;
            margin: 1.5rem 0;
            font-size: 1.05em;
        }
        
        /* Spinner styling */
        .stSpinner {
            display: flex;
            justify-content: center;
            width: 100%;
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
st.title("Resume Skill Extractor")
st.markdown("<p class='description-text'>Upload your resume to extract key skills</p>", unsafe_allow_html=True)

# Create centered container for upload
uploaded_file = st.file_uploader(
    label="Choose a PDF file",
    type="pdf",
    help="Upload a PDF resume to extract skills",
    label_visibility="collapsed"
)

# Display uploaded file information and extract skills
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")
    
    # File metrics in centered columns
    metric_col1, metric_col2, metric_col3 = st.columns([1, 1, 1])
    with metric_col2:
        st.write("")  # Spacer
    with metric_col1:
        st.metric(label="File Name", value=uploaded_file.name)
    with metric_col2:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.metric(label="File Size", value=f"{file_size_mb:.2f} MB")
    with metric_col3:
        st.write("")  # Spacer
    
    st.markdown("---")
    
    # Extract and display skills
    st.markdown("<h2 class='section-header'>🎯 Extracted Skills</h2>", unsafe_allow_html=True)
    
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
                
                # Display skills as a list as well
                with st.expander("📋 View as List"):
                    for i, skill in enumerate(extracted_skills, 1):
                        st.write(f"{i}. {skill}")
            else:
                st.warning("⚠️ No skills found in the resume. Please check the file.")
        else:
            st.error("Could not extract text from PDF.")
    
    st.markdown("---")
    
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

st.markdown("<p class='footer-text'>Supported format: PDF | Secure & Private</p>", unsafe_allow_html=True)
