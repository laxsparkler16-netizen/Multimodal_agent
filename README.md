# Multi-Language Voice Translation App

A web-based application that enables users to record voice input in various Indian languages, transcribe it to text using AWS Kiro Speech-to-Text, and translate the transcribed text to another Indian language using AWS Kiro Translation services.

## Features

- 🎤 Voice recording with browser MediaRecorder API
- 🗣️ Support for 8+ Indian languages (Hindi, Tamil, Telugu, Malayalam, Kannada, Marathi, Bengali, Odia, English)
- 📝 Real-time speech-to-text transcription
- 🌐 Multi-language translation
- 🎨 Clean, modern, and aesthetic UI
- ⚡ Fast and responsive

## Project Structure

```
voice-translation-app/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration and environment variables
│   │   ├── kiro_client.py       # AWS Kiro API client
│   │   ├── audio_processor.py   # Audio format conversion utilities
│   │   └── models.py            # Pydantic request/response models
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Example environment configuration
├── frontend/
│   ├── index.html              # Main application page
│   └── assets/
│       ├── styles.css          # Application styles
│       └── app.js              # Application JavaScript
├── README.md                   # This file
└── .gitignore                  # Git ignore patterns
```

## Prerequisites

- Python 3.9 or higher
- Modern web browser with MediaRecorder API support (Chrome, Firefox, Edge)
- AWS Kiro API credentials

## Setup Instructions

### 1. Obtain AWS Kiro API Credentials

1. Sign in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to AWS Kiro service
3. Create a new API key or use an existing key
4. Copy the API key for use in the next step

**Required IAM Permissions:**

Your AWS IAM user/role needs the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kiro:InvokeModel"
      ],
      "Resource": [
        "arn:aws:kiro:*:*:model/kiro-asr-multilingual-v1",
        "arn:aws:kiro:*:*:model/kiro-translate-indian-languages-v1"
      ]
    }
  ]
}
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your KIRO_API_KEY
# Use your favorite text editor to edit .env
```

**Environment Variables:**

Edit the `.env` file and set:

```
KIRO_API_KEY=your_aws_kiro_api_key_here
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
MAX_AUDIO_SIZE_MB=10
```

### 3. Run the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn src.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### 4. Run the Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Start a simple HTTP server
# Python 3:
python -m http.server 8080

# Or using Python 2:
python -m SimpleHTTPServer 8080
```

Open your browser and navigate to `http://localhost:8080`

## Usage

1. **Select Input Language**: Choose the language you'll speak from the first dropdown
2. **Record Audio**: Click the "Record" button and speak into your microphone
3. **Stop Recording**: Click "Stop" when finished
4. **View Transcription**: The transcribed text will appear automatically
5. **Select Target Language**: Choose the language you want to translate to
6. **Translate**: Click the "Translate" button to see the translation

## API Endpoints

### POST /stt (Speech-to-Text)

Transcribes audio to text.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `audio`: Audio file (WAV, MP3, WebM, etc.)
  - `input_language`: Language code (e.g., "hi-IN", "ta-IN")

**Response:**
```json
{
  "recognized_text": "transcribed text here",
  "success": true
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/stt \
  -F "audio=@sample_audio.wav" \
  -F "input_language=hi-IN"
```

### POST /translate

Translates text from one language to another.

**Request:**
- Content-Type: `application/json`
- Body:
```json
{
  "text": "text to translate",
  "source_language": "hi",
  "target_language": "ta"
}
```

**Response:**
```json
{
  "translated_text": "translated text here",
  "success": true
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते",
    "source_language": "hi",
    "target_language": "ta"
  }'
```

## Supported Languages

### Input Languages (for Speech Recognition)
- English (US) - `en-US`
- Hindi - `hi-IN`
- Tamil - `ta-IN`
- Telugu - `te-IN`
- Kannada - `kn-IN`
- Malayalam - `ml-IN`
- Bengali - `bn-IN`
- Marathi - `mr-IN`

### Target Languages (for Translation)
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
- Ensure your browser has permission to access the microphone
- Check browser settings: Settings → Privacy → Microphone
- Try using HTTPS (required by some browsers for microphone access)

### Backend Connection Error
- Verify the backend server is running on port 8000
- Check CORS settings in `.env` file
- Ensure frontend is accessing the correct backend URL

### AWS Kiro API Errors
- Verify your API key is correct in `.env`
- Check IAM permissions for your AWS account
- Ensure you have sufficient API quota/credits

### Audio Upload Fails
- Check audio file size (max 10MB by default)
- Verify audio format is supported
- Check backend logs for specific error messages

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=src --cov-report=html
```

### API Documentation

When the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Technology Stack

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- MediaRecorder API
- Fetch API

**Backend:**
- Python 3.9+
- FastAPI
- Pydantic
- pydub (audio processing)
- httpx (HTTP client)

**External Services:**
- AWS Kiro Speech-to-Text API
- AWS Kiro Translation API

## License

MIT License - feel free to use this project for learning and development.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
