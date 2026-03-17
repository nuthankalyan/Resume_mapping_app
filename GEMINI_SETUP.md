# Setup Guide for Gemini API Integration

## Getting Started with Job Description Analysis

The Flask application now includes JD (Job Description) analysis powered by Google's Gemini API. Follow these steps to set up and use this feature.

## Prerequisites

- Python 3.8+
- Flask application running
- Google Account (for Gemini API access)

## Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click on "Create API Key"
3. Select your project or create a new one
4. The API key will be generated and displayed
5. Copy the API key

## Step 2: Set Environment Variable

### On Linux/macOS (Terminal):
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### On Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your-api-key-here
```

### On Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

## Step 3: Install Dependencies

```bash
pip install -r requirements-flask.txt
```

This installs:
- `flask==3.0.0`
- `werkzeug==3.0.0`
- `pypdf==3.17.2`
- `google-generativeai==0.3.0`

## Step 4: Run the Application

```bash
python flask_app.py
```

The application will start on `http://localhost:5000`

## Step 5: Access JD Analysis

1. Navigate to the application in your browser
2. Click on "💼 JD Analysis" tab
3. Paste or type your job description
4. Click "🔍 Analyze Job Description"
5. Wait for the analysis to complete

## Features

The JD Analysis feature extracts:

### 1. **Job Title** 📍
- The position title extracted from the job description

### 2. **experience_level** 📅
- Years of experience required (if mentioned)

### 3. **NER Keywords** 🏷️
- Named Entity Recognition keywords (job titles, roles, technologies, tools)
- Displayed as keyword badges

### 4. **Key Responsibilities** 📋
- 5-7 main responsibilities of the position
- Displayed as a numbered list

### 5. **Required Skills** ⚙️
- Technical and soft skills needed for the role
- Displayed as skill badges with blue color scheme

### 6. **Key Technologies** 💻
- Specific technologies and tools mentioned
- Displayed as technology badges with cyan color scheme

### 7. **Qualifications** 🎓
- Educational and professional qualifications needed
- Displayed as a numbered list

## Terminal Output

When a job description is analyzed, detailed information is printed to the terminal in JSON format:

```
================================================================================
JOB DESCRIPTION ANALYSIS RESULTS
================================================================================
{
  "job_title": "Senior Software Engineer",
  "experience_level": "5+ years",
  "ner_keywords": ["Python", "AWS", "Team Lead", ...],
  "key_responsibilities": [...],
  "required_skills": [...],
  "key_technologies": [...],
  "qualifications": [...]
}
================================================================================
```

## Troubleshooting

### Issue: "Gemini API key not configured"
**Solution:** Make sure the `GEMINI_API_KEY` environment variable is set correctly before starting the application.

```bash
# Verify the variable is set
echo $GEMINI_API_KEY  # Linux/macOS
echo %GEMINI_API_KEY%  # Windows CMD
```

### Issue: "Could not parse JSON response"
**Solution:** This might occur if the Gemini API returns an unexpected format. The application will still display the raw response.

### Issue: "Job description is too short"
**Solution:** Provide at least 50 characters of job description text for meaningful analysis.

### Issue: API Rate Limiting
**Solution:** If you exceed the free tier limits, either:
- Wait for the rate limit to reset
- Upgrade to a paid plan
- Visit [Google Cloud Console](https://console.cloud.google.com/)

## API Limits

The free tier of Gemini API includes:
- Up to 60 requests per minute
- Daily usage limits vary by plan
- Check your [usage dashboard](https://aistudio.google.com/app/usage) for current limits

## Best Practices

1. **Comprehensive JDs**: Provide detailed job descriptions for better analysis
2. **Clear Formatting**: Use proper spacing and sections in job descriptions
3. **Specific Requirements**: Mention specific skills, tools, and technologies
4. **Experience Levels**: Clearly state years of experience required

## Example Job Description

```
Senior Python Developer

5+ years of professional software development experience required.

Key Responsibilities:
- Design and implement scalable Python applications
- Lead code reviews and mentor junior developers
- Collaborate with product teams on feature development
- Optimize database queries and improve system performance
- Participate in DevOps and CI/CD improvements

Required Skills:
- Python 3.8+
- SQL and NoSQL databases
- Docker and Kubernetes
- AWS (EC2, S3, Lambda)
- Git and GitHub
- REST APIs
- Agile methodologies

Qualifications:
- Bachelor's degree in Computer Science or related field
- Experience with machine learning frameworks (TensorFlow, PyTorch)
- Experience with microservices architecture
- Strong communication skills

```

## Download Results

After analyzing a job description, you can:
1. **View Results**: See all extracted information on the page
2. **Copy Badges**: Hover over and copy individual badges
3. **Download JSON**: Click "📥 Download Results" to get a JSON file with all extracted information

## Comparing Resume and JD

You can use both features together:
1. Analyze your resume to get your skills
2. Analyze a job description to get required skills
3. Compare the two to see how well you match the position

## Advanced Usage

### Batch Analysis
Currently, the application processes one JD at a time. For batch processing:
1. Analyze each JD separately
2. Download results for each
3. Combine the JSON files for comparison

### Integration with Resume Matching
To match resumes with JDs:
1. Extract skills from resume
2. Extract required skills from JD
3. Identify skill gaps
4. Get recommendations for upskilling

## Support and Feedback

For issues or feature requests:
1. Check the troubleshooting section above
2. Visit the [Gemini API Documentation](https://ai.google.dev/)
3. Report issues in the repository

## Security Notes

- **Never commit** your API key to version control
- Use environment variables to manage sensitive credentials
- Consider rotating API keys periodically
- Monitor your usage to prevent unexpected charges

## Next Steps

1. Set up the environment variable
2. Install dependencies
3. Run the application
4. Start analyzing job descriptions!

Enjoy analyzing job descriptions and finding the perfect match! 🚀
