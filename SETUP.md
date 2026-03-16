# PDF Document Uploader - Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

3. **Access the application:**
   - The app will automatically open in your default browser at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

## Features
- 📄 Simple PDF file upload interface
- ✅ File validation (PDF format only)
- 📊 Display file name and size metrics
- 💾 Save uploaded documents to `uploads/` folder
- 🎨 Clean and user-friendly UI

## Usage
1. Click on the upload area to select a PDF file
2. View the file details after upload
3. Click the "Save Document" button to store the file
4. The file will be saved in the `uploads/` directory

## Notes
- Maximum file size: 200MB (can be adjusted in the code)
- Only PDF files are accepted
- Uploaded files are stored in the `uploads/` folder
