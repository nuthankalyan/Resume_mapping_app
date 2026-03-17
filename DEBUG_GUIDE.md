# JD Analysis Debugging Guide

## Why You're Not Getting Results

The `/analyze-jd` endpoint wasn't returning results due to several issues that have been fixed:

### **Issues Found & Fixed:**

1. **❌ Hardcoded API Key** (CRITICAL)
   - The GEMINI_API_KEY was hardcoded to an invalid/revoked key
   - **Fix:** Now uses environment variable properly

2. **❌ Poor Error Handling**
   - Errors were being silently ignored
   - **Fix:** Enhanced error logging and debugging

3. **❌ No Response Validation**
   - API response wasn't being validated properly
   - **Fix:** Better JSON parsing and fallback handling

4. **❌ Missing Debug Logging**
   - Hard to track what was happening
   - **Fix:** Comprehensive console logging added

---

## Quick Setup Guide

### **Step 1: Get Your API Key**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### **Step 2: Set Environment Variable**

**Linux/macOS:**
```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-actual-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-actual-api-key-here"
```

### **Step 3: Verify Setup (IMPORTANT)**

Run the test script to verify everything works:

```bash
python test_gemini_api.py
```

**Expected output:**
```
================================================================================
GEMINI API TEST SCRIPT
================================================================================

[1] Checking GEMINI_API_KEY environment variable...
✓ API Key found: AIzaSy...XXXXX

[2] Configuring Gemini API...
✓ API configured successfully

[3] Testing API with simple prompt...
✓ Simple test successful

[4] Testing JD Analysis...
✓ JD Analysis response received
✓ JSON parsed successfully

================================================================================
✓ ALL TESTS PASSED!
================================================================================
```

### **Step 4: Run Flask App**

```bash
python flask_app.py
```

### **Step 5: Test in Browser**

1. Go to `http://localhost:5000`
2. Click "💼 JD Analysis"
3. Click "📋 Load Sample JD"
4. Click "🔍 Analyze Job Description"
5. **You should now see results!**

---

## Understanding the Debug Output

When you run the app now, you'll see detailed logging in the terminal:

```
[JD Analysis] Starting analysis for 850 characters...
[JD Analysis] Calling Gemini API...
[JD Analysis] Raw response received: 524 characters
[JD Analysis] Response preview: {
    "job_title": "Senior Python Developer"...
[JD Analysis] Extracted JSON: {
    "job_title": "Senior Python Developer"...
[JD Analysis] JSON parsed successfully

================================================================================
JOB DESCRIPTION ANALYSIS RESULTS
================================================================================
{
  "job_title": "Senior Python Developer",
  "experience_level": "5+ years",
  "ner_keywords": ["Python", "AWS", "Team Lead", ...],
  ...
}
================================================================================
```

---

## Common Issues & Fixes

### **Issue: "API key not configured"**

**Cause:** GEMINI_API_KEY environment variable not set

**Fix:**
```bash
# Verify key is set
echo $GEMINI_API_KEY  # Linux/macOS
echo %GEMINI_API_KEY%  # Windows CMD

# If empty, set it
export GEMINI_API_KEY="your-key-here"
```

### **Issue: "Error analyzing job description: 403"**

**Cause:** API key is invalid or quota exceeded

**Fix:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Check if your API key is still valid
3. Create a new key if needed
4. Update the environment variable
5. Restart the app

### **Issue: Results show "raw_response" instead of parsed data**

**Cause:** JSON parsing failed

**Fix:** Check terminal logs for the raw response and verify API format

### **Issue: "No JSON found in response"**

**Cause:** API returned text instead of JSON

**Fix:** 
1. Run test script: `python test_gemini_api.py`
2. Check if API is working
3. Verify JD text is being sent correctly

---

## Testing Workflow

### **Full Test Suite:**

```bash
# 1. Test API configuration
python test_gemini_api.py

# Expected: All tests pass

# 2. Start Flask app
python flask_app.py

# Expected: "✓ Gemini API configured successfully"

# 3. In another terminal, use curl to test
curl -X POST http://localhost:5000/analyze-jd \
  -H "Content-Type: application/json" \
  -d '{"jd_text": "Senior Python Developer. 5+ years experience. Skills: Python, AWS, Docker. Responsibilities: Build applications, lead team, mentor juniors."}'

# Expected: JSON response with job details
```

### **Using Browser DevTools:**

1. Open browser DevTools (F12)
2. Go to Console tab
3. Go to Network tab
4. Analyze a JD
5. Look for `/analyze-jd` request
6. Check Response tab for JSON data
7. Check Console for any JavaScript errors

---

## Terminal Debug Output Reference

The app now logs 5 levels of detail:

### **Level 1: API Configuration**
```
✓ Gemini API configured successfully
```

### **Level 2: Request Received**
```
[API] /analyze-jd endpoint called
[API] Request data received: 285 bytes
[API] JD text length: 220 characters
```

### **Level 3: API Call**
```
[JD Analysis] Starting analysis for 220 characters...
[JD Analysis] Calling Gemini API...
```

### **Level 4: Response Processing**
```
[JD Analysis] Raw response received: 524 characters
[JD Analysis] Response preview: {
[JD Analysis] Extracted JSON: {...}
[JD Analysis] JSON parsed successfully
```

### **Level 5: Results**
```
JOB DESCRIPTION ANALYSIS RESULTS
{
  "job_title": "...",
  "ner_keywords": [...],
  ...
}
```

---

## If Still Having Issues

1. **Run test script first:**
   ```bash
   python test_gemini_api.py
   ```

2. **Check the terminal output** for error messages

3. **Check browser console (F12)** for JavaScript errors

4. **Check Network tab** in DevTools for response details

5. **Verify API key** is valid:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Your key should be listed
   - If not, create a new one

6. **Restart everything:**
   ```bash
   # Stop Flask app (Ctrl+C)
   # Set API key again
   export GEMINI_API_KEY="your-key"
   # Restart app
   python flask_app.py
   ```

---

## What Changed

### **Code Improvements:**

✅ Fixed hardcoded API key
✅ Enhanced error handling
✅ Added comprehensive logging
✅ Better JSON parsing
✅ Improved endpoint validation
✅ Added test script
✅ Better fallback handling

### **New Features:**

✅ `test_gemini_api.py` - Verify setup works
✅ Detailed console logging
✅ Better error messages
✅ Response validation
✅ Complete debugging guide

---

## Next Steps

1. **Run the test script:**
   ```bash
   python test_gemini_api.py
   ```

2. **If test passes:** Run Flask app and try the UI

3. **If test fails:** Follow the error message to fix the issue

4. **Check terminal logs** while analyzing JDs for detailed debug info

Good luck! 🚀
