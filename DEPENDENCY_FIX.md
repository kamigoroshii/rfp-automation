# Missing Dependencies Fix Guide

## Problem
When running `uvicorn orchestrator.api.main:app --reload --port 8000`, you get:
```
ModuleNotFoundError: No module named 'google'
```

## Root Cause
The `google-generativeai` package is missing from your virtual environment. This package is required by the Copilot module for Gemini AI integration.

---

## Quick Fix

### Option 1: Run the Install Script (Easiest) ⭐

```bash
install_missing_deps.bat
```

This will:
- Install `google-generativeai==0.3.2`
- Verify the installation
- Tell you when it's ready

### Option 2: Manual Installation

In your activated virtual environment, run:

```bash
pip install google-generativeai==0.3.2
```

Then verify:
```bash
python -c "import google.generativeai as genai; print('Success!')"
```

### Option 3: Reinstall All Dependencies

To ensure all dependencies are properly installed:

```bash
pip install -r requirements.txt
```

---

## After Installing

Once the package is installed, restart your server:

```bash
uvicorn orchestrator.api.main:app --reload --port 8000
```

The server should now start successfully!

---

## What Was Fixed

I've updated `requirements.txt` to include:
```
google-generativeai==0.3.2
```

This package is used by:
- **Copilot Module** (`orchestrator/api/routes/copilot.py`) - For AI-powered chat assistance using Google Gemini

---

## Next Potential Issues

After fixing this dependency, you might encounter:

### 1. **Missing GOOGLE_API_KEY**
If you see warnings about missing API key, add to your `.env`:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 2. **Database Connection Issues**
If you haven't set up PostgreSQL yet, see `POSTGRES_SETUP.md`

### 3. **Redis Connection Issues**
Make sure Redis is running:
```bash
redis-server
```

Or install Redis for Windows from: https://github.com/microsoftarchive/redis/releases

---

## Verification Checklist

After installation, verify everything works:

- [ ] `python -c "import google.generativeai"` - No errors
- [ ] Server starts without import errors
- [ ] API docs accessible at http://127.0.0.1:8000/docs
- [ ] Health check works: http://127.0.0.1:8000/health

---

## Still Having Issues?

If you continue to see import errors, try:

1. **Verify virtual environment is activated**:
   ```bash
   where python
   # Should show: F:\eytech\venv\Scripts\python.exe
   ```

2. **Reinstall in clean environment**:
   ```bash
   deactivate
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Check Python version**:
   ```bash
   python --version
   # Should be Python 3.9 or higher
   ```
