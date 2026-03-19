# 🚀 Running Your Voice Translation App

## Current Status: ✅ RUNNING

Your application is currently running with:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:8080

## Open the Application

**Click or copy this URL to your browser:**
```
http://localhost:8080
```

## How to Use the App

1. **Select Input Language** - Choose the language you'll speak (e.g., Hindi, Tamil, English)
2. **Click "Start Recording"** - Allow microphone access when prompted
3. **Speak** - Say something in your selected language
4. **Click "Stop Recording"** - Wait for transcription
5. **Select Target Language** - Choose the language to translate to
6. **Click "Translate"** - See your translation!

## If You Need to Restart

### Stop the Servers
Press `Ctrl+C` in each terminal window

### Start Backend (Terminal 1)
```bash
cd backend
.\venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
python -m http.server 8080
```

## Important Files

- **Backend .env**: `backend/.env` - Add your AWS Kiro API key here
- **Frontend**: `frontend/index.html` - Main application page
- **API Docs**: http://localhost:8000/docs - Interactive API documentation

## Testing the API

### Test Backend Health
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

### Test Speech-to-Text (with audio file)
```bash
curl -X POST http://localhost:8000/stt \
  -F "audio=@sample_audio.wav" \
  -F "input_language=hi-IN"
```

### Test Translation
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hello\",\"source_language\":\"en\",\"target_language\":\"hi\"}"
```

## Supported Languages

### Input Languages (Speech Recognition)
- English (US) - `en-US`
- Hindi - `hi-IN`
- Tamil - `ta-IN`
- Telugu - `te-IN`
- Kannada - `kn-IN`
- Malayalam - `ml-IN`
- Bengali - `bn-IN`
- Marathi - `mr-IN`

### Target Languages (Translation)
- Hindi - `hi`
- Tamil - `ta`
- Telugu - `te`
- Malayalam - `ml`
- Kannada - `kn`
- Marathi - `mr`
- Bengali - `bn`
- Odia - `or`

## Troubleshooting

### Microphone Not Working
- Check browser permissions (click lock icon in address bar)
- Allow microphone access
- Refresh the page

### Backend Not Responding
- Check if backend is running: http://localhost:8000/
- Look for errors in the backend terminal
- Verify virtual environment is activated

### CORS Errors
- Make sure backend is running on port 8000
- Make sure frontend is running on port 8080
- Check `backend/.env` CORS_ORIGINS setting

### AWS Kiro API Errors
- Verify API key in `backend/.env`
- Check IAM permissions
- Review backend terminal logs

## View Logs

### Backend Logs
Check the terminal where you ran `uvicorn` command

### Frontend Logs
Open browser console (F12) → Console tab

## Next Steps

1. ✅ App is running
2. ⚠️ Add AWS Kiro API key to `backend/.env`
3. 🎤 Test recording and transcription
4. 🌐 Test translation
5. 🎉 Enjoy!

---

**Need Help?** Check:
- README.md - Full documentation
- SETUP_GUIDE.md - Setup instructions
- PROJECT_SUMMARY.md - Project overview
- IMPORTANT_NOTE.md - AWS Kiro configuration
