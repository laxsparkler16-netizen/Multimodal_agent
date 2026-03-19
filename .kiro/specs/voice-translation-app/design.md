# Design Document

## Overview

The Voice Translation App is a web-based application that enables users to record voice input in various Indian languages, transcribe it to text using AWS Kiro Speech-to-Text services, and translate the transcribed text to another Indian language using AWS Kiro Translation services. The system follows a client-server architecture with a lightweight HTML/CSS/JavaScript frontend and a Python FastAPI backend that interfaces with AWS Kiro AI services.

The application workflow is:
1. User selects input language and records audio via browser
2. Frontend sends audio blob to backend /stt endpoint
3. Backend converts audio to required format and calls AWS Kiro ASR
4. Transcribed text is displayed to user
5. User selects target language and requests translation
6. Backend calls AWS Kiro Translation API
7. Translated text is displayed to user

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Frontend (HTML/CSS/JS)                   │    │
│  │  - Language Selection Dropdowns                    │    │
│  │  - MediaRecorder API Integration                   │    │
│  │  - Audio Recording Controls                        │    │
│  │  - Text Display Areas                              │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Endpoints                         │    │
│  │  - POST /stt (Speech-to-Text)                     │    │
│  │  - POST /translate (Translation)                   │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Audio Processing Module                  │    │
│  │  - Format Conversion (16kHz WAV mono)            │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │           AWS Kiro Client                          │    │
│  │  - Authentication & Configuration                  │    │
│  │  - API Request Handling                            │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS/API
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS Kiro Services                         │
│  - Speech-to-Text (ASR) Models                              │
│  - Translation Models                                        │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- Pure HTML5 for structure
- CSS3 for styling (modern, aesthetic design)
- Vanilla JavaScript (ES6+) for interactivity
- MediaRecorder API for audio capture
- Fetch API for HTTP requests

**Backend:**
- Python 3.9+
- FastAPI web framework
- Pydantic for data validation
- python-multipart for file uploads
- pydub for audio processing
- python-dotenv for environment configuration
- httpx or requests for AWS Kiro API calls

**External Services:**
- AWS Kiro Speech-to-Text API
- AWS Kiro Translation API

### Project Structure

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
│   ├── assets/
│   │   ├── styles.css          # Application styles
│   │   └── app.js              # Application JavaScript
│   └── favicon.ico             # Application icon (optional)
├── README.md                   # Setup and usage documentation
└── .gitignore                  # Git ignore patterns
```

## Components and Interfaces

### Frontend Components

#### 1. Language Selection Component
- **Input Language Dropdown**: Allows selection of spoken language
  - Options: en-US, hi-IN, ta-IN, te-IN, kn-IN, ml-IN, bn-IN, mr-IN
  - Stores selected value in JavaScript state
  
- **Target Language Dropdown**: Allows selection of translation target
  - Options: Hindi (hi), Tamil (ta), Telugu (te), Malayalam (ml), Kannada (kn), Marathi (mr), Bengali (bn), Odia (or)
  - Stores selected value in JavaScript state

#### 2. Audio Recording Component
- **Record Button**: Initiates audio capture via MediaRecorder API
- **Recording Indicator**: Visual feedback during recording (animated icon/text)
- **Stop Button**: Terminates recording and prepares audio blob
- **Audio State Management**: Tracks recording status (idle, recording, processing)

#### 3. Display Components
- **Transcription Display Area**: Shows recognized text from ASR
- **Translation Display Area**: Shows translated text
- **Status Messages**: Shows loading states, errors, and validation messages

### Backend Components

#### 1. API Endpoints Module (main.py)

**POST /stt**
- **Request**: Multipart form data
  - `audio`: Audio file blob
  - `input_language`: Language code (e.g., "hi-IN")
- **Response**: JSON
  ```json
  {
    "recognized_text": "string",
    "success": true
  }
  ```
- **Error Response**: JSON
  ```json
  {
    "error": "string",
    "success": false
  }
  ```

**POST /translate**
- **Request**: JSON
  ```json
  {
    "text": "string",
    "source_language": "hi",
    "target_language": "ta"
  }
  ```
- **Response**: JSON
  ```json
  {
    "translated_text": "string",
    "success": true
  }
  ```
- **Error Response**: JSON
  ```json
  {
    "error": "string",
    "success": false
  }
  ```

#### 2. Audio Processing Module (audio_processor.py)

**Functions:**
- `convert_to_wav(audio_bytes: bytes) -> bytes`: Converts uploaded audio to 16kHz WAV mono format
- `validate_audio(audio_bytes: bytes) -> bool`: Validates audio file format and size

#### 3. AWS Kiro Client Module (kiro_client.py)

**KiroClient Class:**
- `__init__(api_key: str)`: Initializes client with API credentials
- `transcribe_audio(audio_data: bytes, language: str) -> str`: Calls AWS Kiro ASR API
- `translate_text(text: str, source_lang: str, target_lang: str) -> str`: Calls AWS Kiro Translation API

**API Integration Details:**
- Base URL: `https://api.kiro.aws.amazon.com/v1` (example - actual URL to be confirmed)
- Authentication: Bearer token in Authorization header
- ASR Model ID: `kiro-asr-multilingual-v1` (example)
- Translation Model ID: `kiro-translate-indian-languages-v1` (example)

#### 4. Configuration Module (config.py)

**Settings Class:**
- `KIRO_API_KEY`: AWS Kiro API key from environment
- `CORS_ORIGINS`: Allowed origins for CORS
- `MAX_AUDIO_SIZE`: Maximum audio file size (e.g., 10MB)
- `SUPPORTED_INPUT_LANGUAGES`: List of valid input language codes
- `SUPPORTED_TARGET_LANGUAGES`: List of valid target language codes

## Data Models

### Frontend Data Structures

```javascript
// Application State
const appState = {
  inputLanguage: null,        // Selected input language code
  targetLanguage: null,       // Selected target language code
  isRecording: false,         // Recording status
  audioBlob: null,           // Recorded audio blob
  recognizedText: '',        // Transcribed text
  translatedText: '',        // Translated text
  isProcessing: false        // API call in progress
};

// Language Options
const inputLanguages = [
  { code: 'en-US', label: 'English (US)' },
  { code: 'hi-IN', label: 'Hindi' },
  { code: 'ta-IN', label: 'Tamil' },
  { code: 'te-IN', label: 'Telugu' },
  { code: 'kn-IN', label: 'Kannada' },
  { code: 'ml-IN', label: 'Malayalam' },
  { code: 'bn-IN', label: 'Bengali' },
  { code: 'mr-IN', label: 'Marathi' }
];

const targetLanguages = [
  { code: 'hi', label: 'Hindi' },
  { code: 'ta', label: 'Tamil' },
  { code: 'te', label: 'Telugu' },
  { code: 'ml', label: 'Malayalam' },
  { code: 'kn', label: 'Kannada' },
  { code: 'mr', label: 'Marathi' },
  { code: 'bn', label: 'Bengali' },
  { code: 'or', label: 'Odia' }
];
```

### Backend Data Models

```python
# Pydantic Models (models.py)

class TranscriptionRequest(BaseModel):
    input_language: str
    # audio file handled separately as UploadFile

class TranscriptionResponse(BaseModel):
    recognized_text: str
    success: bool = True

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    success: bool = False
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing all testable properties from the prework analysis, several properties can be consolidated or are redundant:

- Properties 1.3 and 4.3 (language selection storage) can be combined into a single property about state management
- Properties 1.5 and 4.5 (displaying selected language) can be combined into a single UI reflection property
- Properties 3.1, 3.3, 5.1, and 5.2 (API invocation) can be consolidated into properties about correct API parameter passing
- Properties 3.4 and 5.3 (displaying results) can be combined into a single property about UI updates from API responses
- Properties 2.1, 2.2, and 2.3 cover the recording lifecycle and can be tested together
- Many edge cases (1.4, 2.4, 3.5, 4.4, 5.4, 5.5, 7.3) are important but represent specific error conditions rather than universal properties

The consolidated properties below focus on the core behaviors that must hold across all valid inputs while noting that edge cases will be covered by unit tests.

### Correctness Properties

Property 1: Language selection state persistence
*For any* language selection (input or target), when a user selects a language from a dropdown, the application state should store that language code and reflect it in the UI
**Validates: Requirements 1.3, 1.5, 4.3, 4.5**

Property 2: Recording lifecycle completeness
*For any* recording session with a valid input language, starting the recording should activate MediaRecorder, display a recording indicator, and stopping should produce a valid audio blob
**Validates: Requirements 2.1, 2.2, 2.3, 2.5**

Property 3: STT API invocation correctness
*For any* completed audio recording and selected input language, the frontend should send both the audio blob and language code to the /stt endpoint, and the backend should convert the audio to 16kHz WAV mono before calling AWS Kiro ASR with the correct language parameter
**Validates: Requirements 3.1, 3.2, 3.3**

Property 4: Translation API invocation correctness
*For any* transcribed text with valid source and target languages, the frontend should send all three parameters to the /translate endpoint, and the backend should invoke AWS Kiro Translation with the correct language pair
**Validates: Requirements 5.1, 5.2**

Property 5: API response display consistency
*For any* successful API response (transcription or translation), the returned text should be displayed in the appropriate UI text area
**Validates: Requirements 3.4, 5.3**

Property 6: API response format consistency
*For any* request to /stt or /translate endpoints, the response should be valid JSON containing either the result text with success=true or an error message with success=false
**Validates: Requirements 6.3, 6.4**

Property 7: AWS Kiro authentication header inclusion
*For any* AWS Kiro API call (ASR or Translation), the request should include an Authorization header with the API key
**Validates: Requirements 7.4**

Property 8: Interactive element feedback
*For any* interactive UI element (buttons, dropdowns), hovering or focusing should trigger a visual style change
**Validates: Requirements 8.3**

Property 9: Responsive layout preservation
*For any* browser window size above minimum threshold, the UI should maintain usability with all elements accessible and readable
**Validates: Requirements 8.5**

Property 10: Directory structure initialization
*For any* application setup, initializing the project should create the required directory structure (/backend/src, /frontend, /frontend/assets)
**Validates: Requirements 9.3**

## Error Handling

### Frontend Error Handling

1. **Microphone Permission Errors**
   - Catch MediaRecorder API permission denials
   - Display user-friendly message: "Microphone access denied. Please enable microphone permissions."
   - Provide guidance on enabling permissions

2. **Validation Errors**
   - Check input language selected before allowing recording
   - Check target language selected before allowing translation
   - Check transcribed text exists before allowing translation
   - Display validation messages in a dedicated status area

3. **Network Errors**
   - Catch fetch API errors (network failures, timeouts)
   - Display message: "Network error. Please check your connection and try again."
   - Implement retry mechanism for failed requests

4. **API Error Responses**
   - Parse error responses from backend
   - Display specific error messages from backend
   - Clear processing state to allow retry

5. **Audio Recording Errors**
   - Handle MediaRecorder errors during recording
   - Display message: "Recording failed. Please try again."
   - Reset recording state

### Backend Error Handling

1. **Authentication Errors**
   - Validate KIRO_API_KEY exists on startup
   - Return 500 error if AWS Kiro credentials are invalid
   - Log authentication failures for debugging

2. **Audio Processing Errors**
   - Validate uploaded audio file format and size
   - Return 400 error for invalid audio files
   - Handle audio conversion failures gracefully
   - Maximum file size: 10MB

3. **AWS Kiro API Errors**
   - Catch HTTP errors from AWS Kiro services
   - Parse error responses from AWS Kiro
   - Return appropriate HTTP status codes (400 for client errors, 500 for server errors)
   - Log API errors with request details

4. **Validation Errors**
   - Validate input_language is in supported list
   - Validate source_language and target_language are in supported list
   - Return 400 error with descriptive message for invalid parameters

5. **General Exception Handling**
   - Catch all unhandled exceptions
   - Return 500 error with generic message
   - Log full exception details for debugging
   - Never expose internal error details to client

### Error Response Format

All error responses follow consistent JSON structure:
```json
{
  "error": "Human-readable error message",
  "success": false,
  "error_code": "ERROR_TYPE" // optional
}
```

## Testing Strategy

The Voice Translation App will employ a dual testing approach combining unit tests and property-based tests to ensure comprehensive coverage and correctness.

### Unit Testing Approach

Unit tests will verify specific examples, edge cases, and error conditions:

**Frontend Unit Tests (using Jest or similar):**
- Test that language dropdowns populate with correct options on page load
- Test that recording button is disabled when no input language is selected
- Test that translate button is disabled when no target language is selected or no transcribed text exists
- Test error message display for microphone permission denial
- Test API error response handling and display
- Test that CORS requests work from localhost

**Backend Unit Tests (using pytest):**
- Test /stt endpoint exists and accepts correct parameters
- Test /translate endpoint exists and accepts correct parameters
- Test audio conversion to 16kHz WAV mono format with sample audio file
- Test AWS Kiro client initialization with valid credentials
- Test AWS Kiro client initialization failure with missing credentials
- Test error responses for invalid audio files
- Test error responses for unsupported language codes
- Test CORS middleware configuration
- Test that correct model IDs are used in AWS Kiro API calls

**Integration Tests:**
- Test complete STT workflow with mock AWS Kiro responses
- Test complete translation workflow with mock AWS Kiro responses
- Test end-to-end flow from recording to translation with mocked external services

### Property-Based Testing Approach

Property-based tests will verify universal properties across many randomly generated inputs using **Hypothesis** (Python) for backend tests and **fast-check** (JavaScript) for frontend tests where applicable.

**Configuration:**
- Each property-based test will run a minimum of 100 iterations
- Tests will use appropriate generators for different data types
- Each test will be tagged with a comment referencing the design document property

**Backend Property-Based Tests:**

1. **Property 3: STT API invocation correctness**
   - **Feature: voice-translation-app, Property 3: STT API invocation correctness**
   - Generate: random audio bytes, random valid language codes
   - Verify: backend converts audio to 16kHz WAV and calls AWS Kiro with correct language parameter
   - Assertion: AWS Kiro API called with converted audio and matching language code

2. **Property 4: Translation API invocation correctness**
   - **Feature: voice-translation-app, Property 4: Translation API invocation correctness**
   - Generate: random text strings, random valid language pairs
   - Verify: backend calls AWS Kiro Translation with correct parameters
   - Assertion: AWS Kiro API called with exact text and language pair from request

3. **Property 6: API response format consistency**
   - **Feature: voice-translation-app, Property 6: API response format consistency**
   - Generate: random valid and invalid requests
   - Verify: all responses are valid JSON with required fields
   - Assertion: response contains either (recognized_text/translated_text + success=true) or (error + success=false)

4. **Property 7: AWS Kiro authentication header inclusion**
   - **Feature: voice-translation-app, Property 7: AWS Kiro authentication header inclusion**
   - Generate: random API requests
   - Verify: all AWS Kiro API calls include Authorization header
   - Assertion: Authorization header present with correct format "Bearer {api_key}"

**Frontend Property-Based Tests (if applicable):**

1. **Property 1: Language selection state persistence**
   - **Feature: voice-translation-app, Property 1: Language selection state persistence**
   - Generate: random language selections from valid options
   - Verify: state updates and UI reflects selection
   - Assertion: appState contains selected language and UI displays it

2. **Property 8: Interactive element feedback**
   - **Feature: voice-translation-app, Property 8: Interactive element feedback**
   - Generate: random interactive elements
   - Verify: hover/focus triggers style changes
   - Assertion: computed styles differ between normal and hover/focus states

**Test Organization:**
- Backend tests: `backend/tests/test_api.py`, `backend/tests/test_kiro_client.py`, `backend/tests/test_audio_processor.py`
- Frontend tests: `frontend/tests/app.test.js`
- Property-based tests clearly marked with feature and property number in comments
- Each correctness property implemented by a single property-based test

**Testing Requirements:**
- All tests must pass before deployment
- Property-based tests must run minimum 100 iterations
- Mock AWS Kiro API responses for testing to avoid API costs
- Test coverage should exceed 80% for backend code
- Critical paths (recording → transcription → translation) must have integration tests

## Deployment and Configuration

### Environment Configuration

**Required Environment Variables:**
```
KIRO_API_KEY=your_aws_kiro_api_key_here
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
MAX_AUDIO_SIZE_MB=10
```

**Optional Environment Variables:**
```
KIRO_API_BASE_URL=https://api.kiro.aws.amazon.com/v1
KIRO_ASR_MODEL_ID=kiro-asr-multilingual-v1
KIRO_TRANSLATION_MODEL_ID=kiro-translate-indian-languages-v1
LOG_LEVEL=INFO
```

### AWS Kiro Setup

**Obtaining API Credentials:**
1. Sign in to AWS Console
2. Navigate to AWS Kiro service
3. Create a new API key or use existing key
4. Copy the API key to .env file
5. Ensure IAM permissions include:
   - `kiro:InvokeModel` for ASR model
   - `kiro:InvokeModel` for Translation model

**Required IAM Policy:**
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

### Local Development Setup

**Backend Setup:**
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

# Run the server
uvicorn src.main:app --reload --port 8000
```

**Frontend Setup:**
```bash
# Navigate to frontend directory
cd frontend

# Open index.html in browser or use a simple HTTP server
# Python 3:
python -m http.server 8080

# Then open http://localhost:8080 in browser
```

### API Testing with curl

**Test STT Endpoint:**
```bash
curl -X POST http://localhost:8000/stt \
  -F "audio=@sample_audio.wav" \
  -F "input_language=hi-IN"
```

**Test Translation Endpoint:**
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते",
    "source_language": "hi",
    "target_language": "ta"
  }'
```

### Production Considerations

1. **Security:**
   - Use HTTPS in production
   - Implement rate limiting on API endpoints
   - Validate and sanitize all inputs
   - Store API keys securely (use AWS Secrets Manager)
   - Implement proper CORS configuration for production domains

2. **Performance:**
   - Implement caching for translation results
   - Use connection pooling for AWS Kiro API calls
   - Compress audio files before upload
   - Implement request timeouts

3. **Monitoring:**
   - Log all API requests and responses
   - Monitor AWS Kiro API usage and costs
   - Track error rates and types
   - Set up alerts for service failures

4. **Scalability:**
   - Deploy backend on AWS Lambda or ECS
   - Use API Gateway for request routing
   - Implement queue system for long-running transcriptions
   - Consider CDN for frontend assets

## UI/UX Design Specifications

### Color Scheme
- Primary: #4A90E2 (Blue)
- Secondary: #50C878 (Emerald Green)
- Background: #F8F9FA (Light Gray)
- Text: #2C3E50 (Dark Blue-Gray)
- Error: #E74C3C (Red)
- Success: #27AE60 (Green)
- Border: #E0E0E0 (Light Gray)

### Typography
- Font Family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- Headings: 24px, bold, #2C3E50
- Body Text: 16px, normal, #2C3E50
- Labels: 14px, medium, #5A6C7D
- Buttons: 16px, medium, white

### Layout
- Maximum width: 800px
- Centered container with padding
- Card-based design with subtle shadows
- Responsive grid for mobile devices
- Minimum spacing: 16px between elements

### Interactive Elements
- Buttons: Rounded corners (8px), hover effect (darken 10%), active state (scale 0.98)
- Dropdowns: Custom styled with arrow icon, hover highlight
- Text areas: Border on focus, minimum height 100px
- Recording indicator: Animated pulse effect with red color

### Accessibility
- ARIA labels for all interactive elements
- Keyboard navigation support
- High contrast text for readability
- Focus indicators on all interactive elements
- Screen reader friendly status messages
