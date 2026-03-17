# Quick Start Reference

## 🚀 Start Application in 3 Steps

### 1️⃣ Set API Key
```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```
Get key from: https://ai.google.dev/

### 2️⃣ Run Flask App
```bash
python flask_app.py
```

### 3️⃣ Open Browser
```
http://localhost:5000
```

---

## 📖 How to Use

1. **Left Side**: Paste job description (50+ characters)
2. **Right Side**: Upload resume PDF
3. **Click**: "Analyze Job Description" button
4. **View**: Results with match score and breakdown

---

## 🎯 Match Score Legend

| Score | Color | Meaning |
|-------|-------|---------|
| 80-100% | 🟢 Green | Excellent Match |
| 60-79% | 🔵 Blue | Good Match |
| 40-59% | 🟠 Orange | Moderate Match |
| <40% | 🔴 Red | Poor Match |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `flask_app.py` | Main application with all routes |
| `templates/unified.html` | Web interface |
| `static/style.css` | Styling |
| `USER_GUIDE.md` | Detailed guide |

---

## 🔧 Troubleshooting

**API Key not recognized?**
- Verify: `echo $GEMINI_API_KEY`
- Restart Flask app after setting variable

**Resume won't upload?**
- File must be PDF (not Word, etc.)
- Size must be < 200MB
- Should be readable PDF

**No analysis results?**
- Check JD is 50+ characters
- Check browser console (F12) for errors
- Check Flask console for error messages

---

## 📞 Test API

```bash
python test_gemini_api.py
```

---

## 📚 Full Documentation

See `USER_GUIDE.md` and `IMPLEMENTATION_COMPLETE.md`

---

**Version**: 1.0 (January 2025)
