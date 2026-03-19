"""
FastAPI application for Voice Translation App.
Provides endpoints for speech-to-text and translation services.
"""

import logging
import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from .config import settings
from .models import (
    TranscriptionResponse,
    TranslationRequest,
    TranslationResponse,
    TTSRequest,
    ErrorResponse
)
from .kiro_client import get_kiro_client
from .audio_processor import convert_to_wav, validate_audio, detect_audio_format

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Voice Translation App API",
    description="API for multi-language voice input, transcription, and translation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI application initialized")


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Voice Translation App API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post(
    "/stt",
    response_model=TranscriptionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def speech_to_text(
    audio: UploadFile = File(..., description="Audio file to transcribe"),
    input_language: str = Form(..., description="Input language code (e.g., 'hi-IN', 'ta-IN')")
):
    """
    Transcribe audio to text using AWS Kiro Speech-to-Text.
    
    Args:
        audio: Audio file (WAV, MP3, WebM, OGG, etc.)
        input_language: Language code for speech recognition
    
    Returns:
        TranscriptionResponse with recognized text
    
    Raises:
        HTTPException: If validation fails or transcription errors occur
    """
    try:
        logger.info(f"Received STT request for language: {input_language}")
        
        # Validate input language
        if input_language not in settings.SUPPORTED_INPUT_LANGUAGES:
            logger.warning(f"Unsupported input language: {input_language}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported input language: {input_language}. "
                       f"Supported languages: {', '.join(settings.SUPPORTED_INPUT_LANGUAGES)}"
            )
        
        # Read audio file
        audio_bytes = await audio.read()
        logger.debug(f"Received audio file: {len(audio_bytes)} bytes")
        
        # Validate audio
        is_valid, error_message = validate_audio(audio_bytes)
        if not is_valid:
            logger.warning(f"Audio validation failed: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)
        
        # Detect audio format
        try:
            audio_format = detect_audio_format(audio_bytes)
            logger.debug(f"Detected audio format: {audio_format}")
        except Exception as e:
            logger.error(f"Format detection failed: {str(e)}")
            audio_format = "webm"  # Default fallback
        
        # Convert audio to required format (16kHz WAV mono)
        try:
            wav_bytes = convert_to_wav(audio_bytes, source_format=audio_format)
        except Exception as e:
            logger.error(f"Audio conversion failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process audio file: {str(e)}"
            )
        
        # Call AWS Kiro Speech-to-Text
        try:
            kiro_client = get_kiro_client()
            recognized_text = kiro_client.transcribe_audio(wav_bytes, input_language)
            
            if not recognized_text:
                logger.warning("Empty transcription result")
                recognized_text = ""
            
            logger.info(f"Transcription successful: {len(recognized_text)} characters")
            
            return TranscriptionResponse(
                recognized_text=recognized_text,
                success=True
            )
            
        except Exception as e:
            logger.error(f"AWS Kiro transcription error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Transcription service error: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in STT endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post(
    "/translate",
    response_model=TranslationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def translate(request: TranslationRequest):
    """
    Translate text from one language to another using AWS Kiro Translation.
    
    Args:
        request: TranslationRequest with text, source_language, and target_language
    
    Returns:
        TranslationResponse with translated text
    
    Raises:
        HTTPException: If validation fails or translation errors occur
    """
    try:
        logger.info(f"Received translation request: {request.source_language} -> {request.target_language}")
        
        # Validate source language
        if request.source_language not in settings.SUPPORTED_TARGET_LANGUAGES:
            logger.warning(f"Unsupported source language: {request.source_language}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported source language: {request.source_language}. "
                       f"Supported languages: {', '.join(settings.SUPPORTED_TARGET_LANGUAGES)}"
            )
        
        # Validate target language
        if request.target_language not in settings.SUPPORTED_TARGET_LANGUAGES:
            logger.warning(f"Unsupported target language: {request.target_language}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported target language: {request.target_language}. "
                       f"Supported languages: {', '.join(settings.SUPPORTED_TARGET_LANGUAGES)}"
            )
        
        # Validate text is not empty
        if not request.text.strip():
            logger.warning("Empty text provided for translation")
            raise HTTPException(
                status_code=400,
                detail="Text to translate cannot be empty"
            )
        
        # Call AWS Kiro Translation
        try:
            kiro_client = get_kiro_client()
            translated_text = kiro_client.translate_text(
                request.text,
                request.source_language,
                request.target_language
            )
            
            if not translated_text:
                logger.warning("Empty translation result")
                translated_text = ""
            
            logger.info(f"Translation successful: {len(translated_text)} characters")
            
            return TranslationResponse(
                translated_text=translated_text,
                success=True
            )
            
        except Exception as e:
            logger.error(f"AWS Kiro translation error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Translation service error: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in translation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/tts", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def text_to_speech_endpoint(request: TTSRequest):
    """
    Generate speech audio using AI4Bharat Indic-TTS fallback logic.
    """
    try:
        logger.info(f"Received AI4Bharat-Indic-TTS request for language: {request.target_language}")
        
        # We use a fallback to gTTS since true local AI4Bharat-IndicTTS require multi-GB PyTorch models
        # Note: If AI4Bharat Dhruva API credentials were provided, we could hit their API directly here.
        from gtts import gTTS
        
        # Clean language code for generic match
        lang_code = request.target_language.split('-')[0].lower()
        
        tts = gTTS(text=request.text, lang=lang_code, slow=False)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        
        audio_bytes = audio_stream.getvalue()
        logger.info(f"Generated {len(audio_bytes)} bytes of TTS audio")
        
        return Response(content=audio_bytes, media_type="audio/mpeg")
        
    except Exception as e:
        logger.error(f"TTS generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate TTS audio: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "success": False
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom exception handler for general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "success": False
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
