#!/usr/bin/env python3
"""
Test script for Gemini API JD Analysis
Run this to verify your API configuration before running the Flask app
"""

import os
import sys
import json
import google.generativeai as genai

def test_gemini_api():
    """Test Gemini API connection and functionality"""
    
    print("\n" + "="*80)
    print("GEMINI API TEST SCRIPT")
    print("="*80 + "\n")
    
    # Check API key
    print("[1] Checking GEMINI_API_KEY environment variable...")
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set!")
        print("\nSet it with:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return False
    
    print(f"✓ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
    # Configure API
    print("\n[2] Configuring Gemini API...")
    try:
        genai.configure(api_key=api_key)
        print("✓ API configured successfully")
    except Exception as e:
        print(f"❌ ERROR configuring API: {str(e)}")
        return False
    
    # Test simple prompt
    print("\n[3] Testing API with simple prompt...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        test_response = model.generate_content("Say 'API is working' in JSON format: {\"status\": \"message\"}")
        print(f"✓ Simple test successful")
        print(f"  Response: {test_response.text[:100]}...")
    except Exception as e:
        print(f"❌ ERROR testing API: {str(e)}")
        return False
    
    # Test JD analysis
    print("\n[4] Testing JD Analysis...")
    sample_jd = """
    Senior Python Developer
    
    5+ years of experience required.
    
    Key Responsibilities:
    - Develop Python applications
    - Code reviews
    - Mentor junior developers
    
    Required Skills:
    - Python 3.8+
    - Django
    - PostgreSQL
    - Docker
    
    Qualifications:
    - Bachelor's degree
    - 5+ years experience
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Analyze this JD and return JSON with: job_title, experience_level, ner_keywords, key_responsibilities, required_skills, key_technologies, qualifications.

Job Description:
{sample_jd}

Return ONLY valid JSON starting with {{ and ending with }}"""
        
        jd_response = model.generate_content(prompt)
        response_text = jd_response.text.strip()
        
        print(f"✓ JD Analysis response received ({len(response_text)} chars)")
        print(f"  Preview: {response_text[:150]}...")
        
        # Try to parse JSON
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        
        parsed = json.loads(json_str)
        print(f"✓ JSON parsed successfully")
        print(f"  Keys found: {list(parsed.keys())}")
        
    except Exception as e:
        print(f"❌ ERROR in JD analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED!")
    print("="*80)
    print("\nYour Gemini API is configured correctly.")
    print("You can now run: python flask_app.py")
    print("")
    
    return True


if __name__ == '__main__':
    success = test_gemini_api()
    sys.exit(0 if success else 1)
