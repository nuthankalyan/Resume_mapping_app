# Environment Configuration Guide

## Overview

This project uses environment variables to manage sensitive configuration, particularly the Gemini API key. The `.env` file keeps secrets out of version control and makes the application easier to configure across different environments.

---

## Files

### `.env` (Not tracked by Git)
Contains your actual API keys and sensitive configuration.

**Example:**
```
GEMINI_API_KEY=AIzaSyCsTwtrv_fowavpuc5SBrAZMFBt6NSHiAk
```

⚠️ **IMPORTANT**: This file is in `.gitignore` and should NEVER be committed to Git.

### `.env.example` (Tracked by Git)
Template file showing what environment variables are needed. Users can copy this to `.env` and fill in their own values.

**Example:**
```
GEMINI_API_KEY=your-gemini-api-key-here
```

---

## Setup Instructions

### 1. Get Your Gemini API Key

1. Visit: https://ai.google.dev/
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 2. Create Your `.env` File

Option A: Copy from example
```bash
cp .env.example .env
```

Option B: Create manually
```bash
echo "GEMINI_API_KEY=your-key-here" > .env
```

### 3. Edit `.env` with Your API Key

```bash
# Open .env in your editor and replace the placeholder
nano .env
# or
vim .env
# or
code .env
```

Paste your API key:
```
GEMINI_API_KEY=AIzaSyCsTwtrv_fowavpuc5SBrAZMFBt6NSHiAk
```

### 4. Run the Application

The application will automatically load the `.env` file on startup:

```bash
python flask_app.py
```

You'll see:
```
✓ Gemini API configured successfully
```

---

## How It Works

When the Flask app starts:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

The `load_dotenv()` function reads the `.env` file and makes all variables available via `os.getenv()`.

---

## Security Best Practices

✅ **DO:**
- Add `.env` to `.gitignore` (already done)
- Keep `.env` secure and private
- Use `.env.example` as a template in version control
- Rotate API keys regularly
- Use strong, unique API keys

❌ **DON'T:**
- Commit `.env` to Git
- Share `.env` files via email or messaging
- Copy API keys directly in source code
- Use the same key for multiple environments
- Leave `.env` publicly accessible

---

## Environment-Specific Setup

### Local Development
1. Copy `.env.example` to `.env`
2. Add your development API key
3. Run locally: `python flask_app.py`

### Production
1. Set environment variables on your production server/platform
2. For example, on Heroku:
   ```bash
   heroku config:set GEMINI_API_KEY=your-production-key
   ```
3. The application will use these variables automatically

---

## Troubleshooting

### "GEMINI_API_KEY not found in .env file"

**Solution:**
1. Verify `.env` file exists in project root
2. Check file is named exactly `.env` (no extension)
3. Verify the variable name is exactly `GEMINI_API_KEY`
4. Restart the Flask application

```bash
# Verify .env exists
ls -la .env

# Check contents (first few lines)
head -n 5 .env

# Restart app
python flask_app.py
```

### "API key is invalid or revoked"

**Solution:**
1. Verify API key in `.env` is correct and complete
2. Check the key is enabled in Google Cloud Console
3. Regenerate a new key if needed
4. Update `.env` with the new key

### Changes to `.env` not taking effect

**Solution:**
- Restart the Flask application after editing `.env`
- The `.env` file is loaded once at startup

---

## File Structure

```
Resume_mapping_app/
├── .env                  # ← Your API key (NOT in Git)
├── .env.example          # ← Template (in Git)
├── .gitignore            # ← Ignores .env
├── flask_app.py          # ← Loads .env automatically
├── requirements-flask.txt # ← Includes python-dotenv
└── ...
```

---

## Alternative: Export Environment Variable

If you prefer not to use `.env`, you can set the variable directly:

```bash
# Linux/Mac
export GEMINI_API_KEY='your-api-key-here'
python flask_app.py

# Windows (PowerShell)
$env:GEMINI_API_KEY='your-api-key-here'
python flask_app.py

# Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here
python flask_app.py
```

However, using `.env` is recommended as it's more convenient and less error-prone.

---

## API Key Rotation

Periodically rotate your API keys for security:

1. Generate a new API key on ai.google.dev
2. Update `.env`:
   ```
   GEMINI_API_KEY=new-api-key-here
   ```
3. Restart the application
4. Delete the old API key from your Google Cloud account

---

## More Information

- [python-dotenv Documentation](https://python-dotenv.readthedocs.io/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Environment Variables Best Practices](https://12factor.net/config)

---

**Last Updated**: March 2026
