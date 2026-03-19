# Quick Setup Guide

## Step-by-Step Installation

### 1. Prerequisites Check
- [ ] Python 3.9+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Modern web browser (Chrome, Firefox, Edge)
- [ ] AWS Kiro API credentials ready

### 2. Backend Setup (5 minutes)

```bash
# Clone or navigate to project directory
cd voice-translation-app

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows Command Prompt:
venv\Scripts\activate.bat
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env file and add your KIRO_API_KEY
# Use notepad, vim, or any text editor:
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 3. Configure AWS Kiro API Key

Edit the `.env` file and replace `your_aws_kiro_api_key_here` with your actual API key:

```
KIRO_API_KEY=sk-your-actual-api-key-here
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
MAX_AUDIO_SIZE_MB=10
```

### 4. Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn src.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 5. Start Frontend (New Terminal)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd voice-translation-app/frontend

# Start HTTP server
python -m http.server 8080
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

### 6. Open Application

Open your browser and go to:
```
http://localhost:8080
```

## Testing the Application

### Test 1: Check Backend API
Open a new terminal and run:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Voice Translation App API",
  "status": "running",
  "version": "1.0.0"
}
```

### Test 2: Record and Transcribe
1. Select "Hindi" as input language
2. Click "Start Recording"
3. Speak in Hindi: "नमस्ते, मेरा नाम राज है"
4. Click "Stop Recording"
5. Wait for transcription to appear

### Test 3: Translate
1. Select "Tamil" as target language
2. Click "Translate"
3. See translation appear in output area

## Common Issues

### Issue: "Module not found" error
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution:** Change the port number:
```bash
# Backend
uvicorn src.main:app --reload --port 8001

# Frontend
python -m http.server 8081
```

### Issue: "CORS error" in browser
**Solution:** Check that:
1. Backend is running on port 8000
2. Frontend is running on port 8080
3. `.env` file has correct CORS_ORIGINS

### Issue: "Microphone not working"
**Solution:**
1. Check browser permissions (click lock icon in address bar)
2. Allow microphone access
3. Refresh the page

### Issue: "AWS Kiro API error"
**Solution:**
1. Verify API key is correct in `.env`
2. Check IAM permissions
3. Verify API quota/credits

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check API documentation at http://localhost:8000/docs
- Review the code in `backend/src/` and `frontend/assets/`

## Getting AWS Kiro API Credentials

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to AWS Kiro service
3. Click "API Keys" or "Credentials"
4. Create new API key or copy existing one
5. Save the key securely
6. Add to `.env` file

## Support

If you encounter issues:
1. Check the terminal logs for error messages
2. Review the browser console (F12) for frontend errors
3. Verify all prerequisites are installed
4. Ensure ports 8000 and 8080 are available
