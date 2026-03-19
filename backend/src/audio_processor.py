"""
Audio processing utilities for format conversion and validation.
"""

import io
import logging
from typing import Tuple
from .config import settings

logger = logging.getLogger(__name__)

# Note: For production, install ffmpeg and use pydub for proper audio conversion
# For now, we'll pass through the audio as-is and let AWS Kiro handle it


def convert_to_wav(audio_bytes: bytes, source_format: str = "webm") -> bytes:
    """
    Convert audio bytes to 16kHz WAV mono format.
    
    NOTE: This is a simplified version that passes audio through as-is.
    For production, install ffmpeg and pydub for proper audio conversion.
    
    Args:
        audio_bytes: Input audio file bytes
        source_format: Source audio format (webm, mp3, ogg, etc.)
    
    Returns:
        Audio bytes (passed through as-is for now)
    
    Raises:
        Exception: If audio conversion fails
    """
    try:
        logger.info(f"Audio processing: {len(audio_bytes)} bytes ({source_format} format)")
        logger.warning("Audio conversion skipped - using original format. Install ffmpeg and pydub for proper conversion.")
        
        # For now, return audio as-is
        # AWS Kiro should be able to handle various audio formats
        return audio_bytes
        
    except Exception as e:
        logger.error(f"Audio processing failed: {str(e)}")
        raise Exception(f"Failed to process audio: {str(e)}")


def validate_audio(audio_bytes: bytes) -> Tuple[bool, str]:
    """
    Validate audio file format and size.
    
    NOTE: This is a simplified version that only checks size.
    For production, install ffmpeg and pydub for proper validation.
    
    Args:
        audio_bytes: Audio file bytes to validate
    
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if audio is valid, False otherwise
        - error_message: Empty string if valid, error description if invalid
    """
    try:
        # Check file size
        audio_size = len(audio_bytes)
        max_size = settings.max_audio_size_bytes
        
        if audio_size == 0:
            return False, "Audio file is empty"
        
        if audio_size > max_size:
            max_mb = settings.MAX_AUDIO_SIZE_MB
            actual_mb = audio_size / (1024 * 1024)
            return False, f"Audio file too large: {actual_mb:.2f}MB (max: {max_mb}MB)"
        
        logger.info(f"Audio validation successful: {audio_size} bytes")
        return True, ""
        
    except Exception as e:
        logger.error(f"Audio validation error: {str(e)}")
        return False, f"Audio validation failed: {str(e)}"


def detect_audio_format(audio_bytes: bytes) -> str:
    """
    Detect the format of audio bytes.
    
    Args:
        audio_bytes: Audio file bytes
    
    Returns:
        Detected format string (e.g., "webm", "wav", "mp3")
    
    Raises:
        Exception: If format cannot be detected
    """
    # Check file signatures (magic numbers)
    if len(audio_bytes) < 12:
        raise Exception("Audio file too small to detect format")
    
    # WAV: RIFF....WAVE
    if audio_bytes[:4] == b'RIFF' and audio_bytes[8:12] == b'WAVE':
        return "wav"
    
    # MP3: ID3 or 0xFF 0xFB
    if audio_bytes[:3] == b'ID3' or (audio_bytes[0] == 0xFF and audio_bytes[1] & 0xE0 == 0xE0):
        return "mp3"
    
    # OGG: OggS
    if audio_bytes[:4] == b'OggS':
        return "ogg"
    
    # WebM/Matroska: 0x1A 0x45 0xDF 0xA3
    if audio_bytes[:4] == b'\x1A\x45\xDF\xA3':
        return "webm"
    
    # M4A/MP4: ftyp
    if audio_bytes[4:8] == b'ftyp':
        return "m4a"
    
    # Default to webm (common for browser recordings)
    logger.warning("Could not detect audio format, defaulting to webm")
    return "webm"
