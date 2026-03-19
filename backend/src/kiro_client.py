"""
AWS Kiro API client for speech-to-text and translation services.
"""

import httpx
import logging
import os
from typing import Optional
from .config import settings
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Check if we should use mock mode (for testing without real API)
USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "true").lower() == "true"


class KiroClient:
    """Client for interacting with AWS Kiro AI services."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Kiro client with API credentials.
        
        Args:
            api_key: AWS Kiro API key. If not provided, uses settings.KIRO_API_KEY
        """
        self.api_key = api_key or settings.KIRO_API_KEY
        self.base_url = settings.KIRO_API_BASE_URL
        self.asr_model_id = settings.KIRO_ASR_MODEL_ID
        self.translation_model_id = settings.KIRO_TRANSLATION_MODEL_ID
        
        if not self.api_key:
            logger.error("AWS Kiro API key is missing")
            raise ValueError("KIRO_API_KEY is required but not provided")
        
        # Initialize HTTP client with default headers
        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self._get_auth_headers(),
            timeout=30.0
        )
        
        logger.info("AWS Kiro client initialized successfully")
    
    def _get_auth_headers(self) -> dict:
        """
        Get authentication headers for AWS Kiro API requests.
        
        Returns:
            Dictionary containing Authorization header with Bearer token
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """
        Transcribe audio to text using AWS Kiro Speech-to-Text API.
        
        Args:
            audio_data: Audio file bytes in WAV format (16kHz mono)
            language: Language code for speech recognition (e.g., "hi-IN", "ta-IN")
        
        Returns:
            Transcribed text string
        
        Raises:
            httpx.HTTPError: If the API request fails
            ValueError: If the response format is invalid
        """
        logger.info(f"Transcribing audio with language: {language}")
        
        # MOCK MODE: Return demo transcription for testing
        if USE_MOCK_MODE:
            logger.warning("🎭 MOCK MODE: Returning demo transcription")
            mock_transcriptions = {
                "en-US": "Hello, this is a demo transcription in English. The actual AWS Kiro API is not configured.",
                "hi-IN": "नमस्ते, यह हिंदी में एक डेमो ट्रांसक्रिप्शन है। वास्तविक AWS Kiro API कॉन्फ़िगर नहीं है।",
                "ta-IN": "வணக்கம், இது தமிழில் ஒரு டெமோ டிரான்ஸ்கிரிப்ஷன் ஆகும். உண்மையான AWS Kiro API கட்டமைக்கப்படவில்லை.",
                "te-IN": "నమస్కారం, ఇది తెలుగులో ఒక డెమో ట్రాన్స్క్రిప్షన్. అసలు AWS Kiro API కాన్ఫిగర్ చేయబడలేదు.",
                "kn-IN": "ನಮಸ್ಕಾರ, ಇದು ಕನ್ನಡದಲ್ಲಿ ಡೆಮೊ ಟ್ರಾನ್ಸ್‌ಕ್ರಿಪ್ಷನ್ ಆಗಿದೆ. ನಿಜವಾದ AWS Kiro API ಕಾನ್ಫಿಗರ್ ಮಾಡಲಾಗಿಲ್ಲ.",
                "ml-IN": "നമസ്കാരം, ഇത് മലയാളത്തിൽ ഒരു ഡെമോ ട്രാൻസ്ക്രിപ്ഷൻ ആണ്. യഥാർത്ഥ AWS Kiro API കോൺഫിഗർ ചെയ്തിട്ടില്ല.",
                "bn-IN": "নমস্কার, এটি বাংলায় একটি ডেমো ট্রান্সক্রিপশন। প্রকৃত AWS Kiro API কনফিগার করা হয়নি।",
                "mr-IN": "नमस्कार, हे मराठीत एक डेमो ट्रान्सक्रिप्शन आहे. वास्तविक AWS Kiro API कॉन्फिगर केलेले नाही."
            }
            return mock_transcriptions.get(language, "This is a demo transcription. Configure AWS Kiro API for real transcription.")
        
        try:
            # Prepare request payload for AWS Kiro ASR
            # Note: This is a placeholder implementation
            # Actual AWS Kiro API format may differ
            payload = {
                "model_id": self.asr_model_id,
                "language": language,
                "audio_format": "wav",
                "sample_rate": 16000,
                "audio_data": audio_data.hex()  # Convert bytes to hex string
            }
            
            response = self.client.post(
                "/asr/transcribe",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            transcribed_text = result.get("transcription", "")
            
            if not transcribed_text:
                logger.warning("Empty transcription received from AWS Kiro")
                return ""
            
            logger.info(f"Transcription successful: {len(transcribed_text)} characters")
            return transcribed_text
            
        except httpx.HTTPError as e:
            logger.error(f"AWS Kiro ASR API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during transcription: {str(e)}")
            raise
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using Google Translate (Free).
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., "hi", "ta", "en")
            target_lang: Target language code (e.g., "hi", "ta", "en")
        
        Returns:
            Translated text string
        
        Raises:
            Exception: If translation fails
        """
        logger.info(f"Translating text from {source_lang} to {target_lang}")
        logger.info(f"Text to translate: {text[:100]}...")  # Log first 100 chars
        
        try:
            # Use Google Translate for real translation
            logger.info("🌐 Using Google Translate (deep-translator) for real translation")
            
            # Create translator instance
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            # Translate the text
            translated_text = translator.translate(text)
            
            if not translated_text:
                logger.warning("Empty translation received from Google Translate")
                return text  # Return original text if translation fails
            
            logger.info(f"✅ Translation successful: {translated_text[:100]}...")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Google Translate error: {str(e)}")
            logger.warning("Falling back to original text")
            # Return original text if translation fails
            return f"[Translation Error] {text}"
    
    def close(self):
        """Close the HTTP client connection."""
        self.client.close()
        logger.info("AWS Kiro client closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global client instance
_kiro_client: Optional[KiroClient] = None


def get_kiro_client() -> KiroClient:
    """
    Get or create the global Kiro client instance.
    
    Returns:
        KiroClient instance
    """
    global _kiro_client
    if _kiro_client is None:
        _kiro_client = KiroClient()
    return _kiro_client
