# Resume to Job Description Matcher - User Guide

## Overview

This application analyzes your resume against a job description to determine how well you match the role. It uses Google's Gemini LLM to intelligently extract information from both documents and provides a detailed match score.

## Features

- **Job Description Analysis**: Extract key details like position title, required skills, technologies, experience level, etc.
- **Resume Intelligence Analysis**: Uses Gemini AI to extract candidate information from resume text
- **Smart Matching**: Calculates match score based on:
  - Skills match (60% weight)
  - Technologies match (30% weight)
  - Experience level match (10% weight)
- **Visual Feedback**: Color-coded match score (Green=Excellent, Blue=Good, Orange=Moderate, Red=Poor)
- **Detailed Breakdown**: Shows matched skills, missing skills, matched technologies, and missing technologies

## Prerequisites

1. **Gemini API Key**: You need a Google Gemini API key
   - Get it from: https://ai.google.dev/

2. **Python 3.8+**: The application requires Python 3.8 or higher

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements-flask.txt
   ```

2. **Set Environment Variable** (Important!):
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```
   
   Or on Windows:
   ```bash
   set GEMINI_API_KEY=your-api-key-here
   ```

## Running the Application

1. **Start Flask Server**:
   ```bash
   python flask_app.py
   ```
   
   The app will start on `http://localhost:5000`

2. **Open in Browser**:
   - Navigate to `http://localhost:5000`

## How to Use

### Step 1: Input Job Description
1. Scroll to the **"Job Description"** section on the left
2. Copy and paste the job description text into the textarea
3. The text counter shows character count (minimum 50 characters required)
4. Click **"Analyze Job Description"** button

### Step 2: Upload Your Resume
1. In the **"Your Resume"** section on the right, click the file upload area
   - You can drag and drop a PDF file
   - Or click to browse and select a file
2. Click **"Upload Resume"** button
3. The app will analyze your resume and extract information

### Step 3: View Results
Once both resume and job description are processed, you'll see:

- **Resume Analysis**: Your extracted information (name, experience, skills, technologies, etc.)
- **Job Description Analysis**: Position details and requirements
- **Match Score**: A visual score (0-100) with color coding:
  - **80-100% Green**: Excellent Match
  - **60-79% Blue**: Good Match
  - **40-59% Orange**: Moderate Match
  - **<40% Red**: Poor Match
- **Detailed Breakdown**: Shows:
  - ✓ Matched Skills (green badges)
  - ✗ Missing Skills (red badges)
  - ✓ Matched Technologies (green badges)
  - ✗ Missing Technologies (red badges)

## File Specifications

- **Resume Format**: PDF files only
- **Maximum Size**: 200MB per file
- **Job Description**: Text (no file upload, paste directly)
- **Minimum JD Length**: 50 characters

## Troubleshooting

### API Key Issues
If you see "API key not configured" error:
1. Verify you've set the GEMINI_API_KEY environment variable
2. Make sure the API key is valid (get it from https://ai.google.dev/)
3. Restart the Flask server after setting the environment variable

### Upload Issues
1. Ensure the file is a PDF (not DOC, DOCX, etc.)
2. Check file size is less than 200MB
3. Verify the PDF is readable and not corrupted

### Analysis Not Working
1. Check browser console for error messages (F12 → Console)
2. Check Flask server console output for detailed error logs
3. Ensure JD text is at least 50 characters
4. Make sure Gemini API is working (test with `test_gemini_api.py`)

## Testing the API

Run the test script to verify Gemini API is working:
```bash
python test_gemini_api.py
```

## Application Structure

```
Resume_mapping_app/
├── flask_app.py                 # Main Flask application
├── templates/
│   └── unified.html            # Single-page interface
├── static/
│   └── style.css               # Styling
├── uploads/                     # Temporary resume storage
├── requirements-flask.txt      # Python dependencies
└── test_gemini_api.py          # API test utility
```

## Key Technologies

- **Backend**: Flask (Python web framework)
- **LLM**: Google Gemini 2.5-flash
- **PDF Processing**: pypdf library
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful endpoints with JSON

## Tips for Best Results

1. **Resume**: Ensure it's a well-formatted PDF with clear sections
2. **Job Description**: Use the complete job posting, not just highlights
3. **Skills**: List all relevant skills, certifications, and technologies
4. **Experience**: Include years of experience for better matching

## Support

For issues or questions, check the debug logs in the Flask server console for detailed information about what the API is processing.

---

**Last Updated**: January 2025
