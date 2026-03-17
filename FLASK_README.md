# Resume Skill Extractor - Flask Version

This is a Flask web application that extracts key skills from PDF resumes using pattern matching with a comprehensive skills list.

## Features

- **PDF Upload**: Upload PDF resumes with drag-and-drop support
- **Skill Extraction**: Automatically extracts technical and professional skills from resumes
- **Interactive UI**: Modern, responsive web interface
- **Skill Badges**: Display extracted skills as visually appealing badges
- **File Management**: Save uploaded resumes for future reference
- **File Size Support**: Handles files up to 200MB

## Project Structure

```
Resume_mapping_app/
├── flask_app.py                 # Main Flask application
├── templates/
│   ├── index.html              # Upload form page
│   └── results.html            # Results display page
├── static/
│   └── style.css               # Global stylesheet
├── uploads/                    # Directory for saved resumes
├── requirements-flask.txt      # Flask dependencies
└── FLASK_README.md            # This file
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements-flask.txt
```

Or install manually:
```bash
pip install flask==3.0.0 werkzeug==3.0.0 pypdf==3.17.2
```

### 2. Run the Application

```bash
python flask_app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Open the Application**: Navigate to `http://localhost:5000` in your web browser
2. **Upload Resume**: 
   - Drag and drop a PDF file onto the upload box, or
   - Click "Browse files" and select a PDF file
3. **View Results**: The page will automatically show:
   - Total number of skills found
   - Interactive skill badges
   - List view option for all skills
4. **Save Resume**: Click "💾 Save Resume" to save the PDF to the `uploads/` folder
5. **Upload Another**: Click "📤 Upload Another" to process another resume

## Supported Skills

The application recognizes over 100 common skills across multiple categories:

- **Programming Languages**: Python, Java, JavaScript, C++, C#, PHP, Ruby, Go, Rust, TypeScript, etc.
- **Web Development**: HTML, CSS, React, Angular, Vue, Node.js, Django, Flask, etc.
- **Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, etc.
- **Data Science & ML**: Machine Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-learn, etc.
- **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Terraform, etc.
- **Tools & Frameworks**: Git, GitHub, JIRA, Figma, VS Code, Visual Studio, etc.

## Configuration

Edit the `COMMON_SKILLS` dictionary in `flask_app.py` to add, remove, or modify recognized skills.

### Key Settings

- **MAX_FILE_SIZE**: Set to 200MB (200 * 1024 * 1024 bytes)
- **UPLOAD_FOLDER**: Files are saved in the `uploads/` directory
- **PORT**: Application runs on port 5000 (can be changed in the last line)

## API Endpoints

### POST /upload
Upload and process a PDF file.

**Request**: Multipart form data with file field
**Response**: JSON with extracted skills and file information

### GET /results
Display results page with extracted skills.

**Parameters**: 
- `filename`: Name of uploaded file
- `file_size`: Size of file in MB
- `skills`: List of extracted skills

### POST /save-resume
Save the processed resume.

**Request**: JSON with filename
**Response**: JSON confirmation

## Error Handling

The application handles:
- Invalid file types (only PDF files allowed)
- File size limits (max 200MB)
- PDF extraction errors
- Missing or corrupted files

## Browser Compatibility

Works on all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Deployment

To deploy to production:

1. Set Flask to production mode:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
   ```

3. For cloud deployment (Heroku, AWS, Azure, etc.), follow platform-specific guidelines

## File Storage

- Uploaded files are saved in the `uploads/` directory
- Ensure the directory has proper permissions (755 or similar)
- Consider implementing cleanup routines for old files in production

## Performance Tips

- Use a reverse proxy (Nginx) for static file serving
- Enable gzip compression for CSS/JS files
- Implement caching headers for static assets
- Consider async file processing for large volumes

## Troubleshooting

### Application won't start
- Check if port 5000 is already in use
- Ensure all dependencies are installed: `pip install -r requirements-flask.txt`

### No skills extracted
- Verify the PDF is readable and contains text
- Check if skill names match the predefined COMMON_SKILLS list
- Ensure PDF is not image-based (OCR not supported)

### File upload fails
- Check file size (max 200MB)
- Ensure uploads folder exists and has write permissions
- Verify file is actually a PDF

## Migration from Streamlit

If you were previously using the Streamlit version:
- The core skill extraction logic remains the same
- The UI has been redesigned for a faster, more responsive experience
- Flask provides better deployment flexibility
- No dependency on Streamlit for production environments

## License

[Add your license here]

## Support

For issues or feature requests, please create an issue in the repository.
