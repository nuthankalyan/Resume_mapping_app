from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from pypdf import PdfReader
import os
import re
import google.generativeai as genai
import json

app = Flask(__name__)

# Configure Gemini API
# You'll need to set the GEMINI_API_KEY environment variable
GEMINI_API_KEY = "AIzaSyCsTwtrv_fowavpuc5SBrAZMFBt6NSHiAk"
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✓ Gemini API configured successfully")
else:
    print("✗ Warning: GEMINI_API_KEY environment variable not set. Analysis will not work.")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return None


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


def analyze_job_description(jd_text):
    """Analyze job description using Gemini API to extract key information"""
    if not GEMINI_API_KEY:
        return {
            'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable.'
        }
    
    try:
        print(f"\n[JD Analysis] Starting analysis for {len(jd_text)} characters...")
        
        # Create the prompt for Gemini
        prompt = f"""Analyze the following job description and extract the following information in JSON format:

Job Description:
{jd_text}

Please extract and provide in JSON format:
{{
    "job_title": "The position title",
    "experience_level": "Years of experience required",
    "ner_keywords": ["list", "of", "keywords", "like", "Python", "AWS", "Team Lead"],
    "key_responsibilities": ["responsibility 1", "responsibility 2", "responsibility 3"],
    "required_skills": ["skill 1", "skill 2", "skill 3"],
    "key_technologies": ["tech 1", "tech 2", "tech 3"],
    "qualifications": ["qualification 1", "qualification 2"]
}}

IMPORTANT: Return ONLY valid JSON, no other text. Start with {{ and end with }}"""

        # Call Gemini API
        print("[JD Analysis] Calling Gemini API...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        print(f"[JD Analysis] Raw response received: {len(response_text)} characters")
        print(f"[JD Analysis] Response preview: {response_text[:200]}...")
        
        # Try to extract JSON from response
        jd_analysis = None
        try:
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            print(f"[JD Analysis] Extracted JSON: {json_str[:200]}...")
            
            jd_analysis = json.loads(json_str)
            print("[JD Analysis] JSON parsed successfully")
            
        except (json.JSONDecodeError, ValueError) as json_err:
            print(f"[JD Analysis] JSON parsing error: {str(json_err)}")
            print(f"[JD Analysis] Attempting raw response mapping...")
            
            # Fallback: return response as is
            jd_analysis = {
                'job_title': 'Unable to parse',
                'experience_level': 'Unable to parse',
                'ner_keywords': [],
                'key_responsibilities': [],
                'required_skills': [],
                'key_technologies': [],
                'qualifications': [],
                'raw_response': response_text
            }
        
        # Print to terminal for debugging
        print("\n" + "="*80)
        print("JOB DESCRIPTION ANALYSIS RESULTS")
        print("="*80)
        print(json.dumps(jd_analysis, indent=2))
        print("="*80 + "\n")
        
        return jd_analysis
    
    except Exception as e:
        error_msg = f"Error analyzing job description: {str(e)}"
        print(f"\n[JD Analysis] ERROR: {error_msg}\n")
        print(f"[JD Analysis] Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        return {
            'error': error_msg,
            'details': str(e),
            'type': type(e).__name__
        }


def analyze_resume_text(resume_text):
    """Analyze resume text using Gemini API to extract key information"""
    if not GEMINI_API_KEY:
        return {
            'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable.'
        }
    
    try:
        print(f"\n[Resume Analysis] Starting analysis for {len(resume_text)} characters...")
        
        # Create the prompt for Gemini
        prompt = f"""Analyze the following resume and extract the following information in JSON format:

Resume:
{resume_text}

Please extract and provide in JSON format:
{{
    "candidate_name": "Name of the candidate",
    "experience_level": "Years of experience",
    "skills": ["skill 1", "skill 2", "skill 3", ...],
    "technical_skills": ["tech skill 1", "tech skill 2", ...],
    "key_technologies": ["technology 1", "technology 2", ...],
    "qualifications": ["qualification 1", "qualification 2", ...],
    "work_experience": ["company1", "company2", "position", ...],
    "certifications": ["cert1", "cert2", ...]
}}

IMPORTANT: Return ONLY valid JSON, no other text. Start with {{ and end with }}"""

        # Call Gemini API
        print("[Resume Analysis] Calling Gemini API...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        print(f"[Resume Analysis] Raw response received: {len(response_text)} characters")
        
        # Try to extract JSON from response
        resume_analysis = None
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            resume_analysis = json.loads(json_str)
            print("[Resume Analysis] JSON parsed successfully")
            
        except (json.JSONDecodeError, ValueError) as json_err:
            print(f"[Resume Analysis] JSON parsing error: {str(json_err)}")
            resume_analysis = {
                'candidate_name': 'Unknown',
                'experience_level': 'Unknown',
                'skills': [],
                'technical_skills': [],
                'key_technologies': [],
                'qualifications': [],
                'work_experience': [],
                'certifications': []
            }
        
        print("\n" + "="*80)
        print("RESUME ANALYSIS RESULTS")
        print("="*80)
        print(json.dumps(resume_analysis, indent=2))
        print("="*80 + "\n")
        
        return resume_analysis
    
    except Exception as e:
        error_msg = f"Error analyzing resume: {str(e)}"
        print(f"\n[Resume Analysis] ERROR: {error_msg}\n")
        import traceback
        traceback.print_exc()
        
        return {
            'error': error_msg,
            'details': str(e),
            'type': type(e).__name__
        }


def calculate_match_score(resume_analysis, jd_analysis):
    """Calculate match score between resume and job description"""
    try:
        print("\n[Matching] Starting match score calculation...")
        
        score = 0
        max_score = 0
        details = {
            'skills_match': [],
            'technology_match': [],
            'missing_skills': [],
            'missing_technologies': []
        }
        
        # Extract lists from analysis
        resume_skills = set([s.lower() for s in resume_analysis.get('skills', [])])
        resume_technologies = set([t.lower() for t in resume_analysis.get('key_technologies', [])])
        
        jd_skills = set([s.lower() for s in jd_analysis.get('required_skills', [])])
        jd_technologies = set([t.lower() for t in jd_analysis.get('key_technologies', [])])
        
        # Skills matching (60% weight)
        if jd_skills:
            max_score += 60
            matched_skills = resume_skills & jd_skills
            skill_match_percentage = (len(matched_skills) / len(jd_skills)) * 60
            score += skill_match_percentage
            details['skills_match'] = list(matched_skills)
            details['missing_skills'] = list(jd_skills - resume_skills)
            print(f"[Matching] Skills match: {skill_match_percentage:.1f}/60")
        
        # Technologies matching (30% weight)
        if jd_technologies:
            max_score += 30
            matched_techs = resume_technologies & jd_technologies
            tech_match_percentage = (len(matched_techs) / len(jd_technologies)) * 30
            score += tech_match_percentage
            details['technology_match'] = list(matched_techs)
            details['missing_technologies'] = list(jd_technologies - resume_technologies)
            print(f"[Matching] Technology match: {tech_match_percentage:.1f}/30")
        
        # Experience level matching (10% weight)
        max_score += 10
        resume_exp = resume_analysis.get('experience_level', '').lower()
        jd_exp = jd_analysis.get('experience_level', '').lower()
        
        if resume_exp and jd_exp:
            # Simple heuristic: if resume experience >= JD requirement
            resume_years = ''.join(filter(str.isdigit, resume_exp.split('+')[0]))
            jd_years = ''.join(filter(str.isdigit, jd_exp.split('+')[0]))
            
            if resume_years and jd_years:
                try:
                    if int(resume_years) >= int(jd_years):
                        score += 10
                        print(f"[Matching] Experience match: 10/10")
                except:
                    score += 5
                    print(f"[Matching] Experience match: 5/10 (partial)")
            else:
                score += 5
        
        # Calculate final percentage
        final_score = (score / max_score * 100) if max_score > 0 else 0
        
        print(f"[Matching] Final match score: {final_score:.1f}%")
        print(f"[Matching] Points: {score:.1f}/{max_score}")
        
        # Determine suitability
        if final_score >= 80:
            suitability = "Excellent Match"
            recommendation = "Highly recommended. Candidate meets most requirements."
            color = "green"
        elif final_score >= 60:
            suitability = "Good Match"
            recommendation = "Good fit. Candidate has most required skills."
            color = "blue"
        elif final_score >= 40:
            suitability = "Moderate Match"
            recommendation = "Fair fit. Candidate has some required skills but may need training."
            color = "orange"
        else:
            suitability = "Poor Match"
            recommendation = "Not recommended. Significant skill gaps."
            color = "red"
        
        return {
            'match_score': round(final_score, 1),
            'suitability': suitability,
            'recommendation': recommendation,
            'color': color,
            'details': details,
            'total_points': round(score, 1),
            'max_points': round(max_score, 1)
        }
    
    except Exception as e:
        error_msg = f"Error calculating match score: {str(e)}"
        print(f"\n[Matching] ERROR: {error_msg}\n")
        return {
            'error': error_msg,
            'match_score': 0,
            'suitability': 'Error'
        }


@app.route('/')
def index():
    """Home page with unified resume and JD analysis"""
    return render_template('unified.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume file upload and analysis"""
    print("\n[API] /upload endpoint called")
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)
        
        if resume_text is None:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Analyze resume using LLM
        resume_analysis = analyze_resume_text(resume_text)
        
        if 'error' in resume_analysis:
            return jsonify(resume_analysis), 400
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_size': f"{file_size:.2f}",
            'resume_analysis': resume_analysis
        }), 200
    
    except Exception as e:
        error_msg = f"Error processing resume: {str(e)}"
        print(f"[API] ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/analyze-jd', methods=['POST'])
def analyze_jd():
    """Analyze job description and optionally match with resume"""
    print("\n[API] /analyze-jd endpoint called")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        jd_text = data.get('jd_text', '').strip()
        resume_analysis = data.get('resume_analysis')
        
        if not jd_text:
            return jsonify({'error': 'Job description text is required'}), 400
        
        if len(jd_text) < 50:
            return jsonify({'error': 'Job description is too short. Please provide more details.'}), 400
        
        # Analyze the JD
        jd_analysis = analyze_job_description(jd_text)
        
        if 'error' in jd_analysis:
            return jsonify(jd_analysis), 400
        
        result = {'jd_analysis': jd_analysis}
        
        # If resume analysis is provided, calculate match score
        if resume_analysis and not ('error' in resume_analysis):
            match_result = calculate_match_score(resume_analysis, jd_analysis)
            result['match'] = match_result
        
        return jsonify(result), 200
        
    except Exception as e:
        error_msg = f"Error in analysis: {str(e)}"
        print(f"[API] ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File is too large. Maximum size is 200MB'}), 413


if __name__ == '__main__':
    app.run(debug=True, port=5000)
