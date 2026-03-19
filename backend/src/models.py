"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TranscriptionResponse(BaseModel):
    """Response model for speech-to-text transcription."""
    recognized_text: str = Field(..., description="The transcribed text from audio")
    success: bool = Field(default=True, description="Indicates if the operation was successful")


class TranslationRequest(BaseModel):
    """Request model for text translation."""
    text: str = Field(..., description="Text to translate", min_length=1)
    source_language: str = Field(..., description="Source language code (e.g., 'hi', 'ta')")
    target_language: str = Field(..., description="Target language code (e.g., 'hi', 'ta')")


class TTSRequest(BaseModel):
    """Request model for Text-to-Speech using AI4Bharat Indic-TTS fallback."""
    text: str = Field(..., description="Text to synthesize", min_length=1)
    target_language: str = Field(..., description="Language code (e.g., 'hi', 'ta')")


class TranslationResponse(BaseModel):
    """Response model for text translation."""
    translated_text: str = Field(..., description="The translated text")
    success: bool = Field(default=True, description="Indicates if the operation was successful")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error message")
    success: bool = Field(default=False, description="Indicates if the operation was successful")
    error_code: Optional[str] = Field(None, description="Optional error code for categorization")
