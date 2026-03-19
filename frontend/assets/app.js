/**
 * Voice Translation App - Frontend JavaScript
 * Handles audio recording, transcription, and translation
 */

// ===================================
// Configuration
// ===================================
const API_BASE_URL = 'http://localhost:8000';

// ===================================
// Application State
// ===================================
const appState = {
    inputLanguage: null,
    targetLanguage: null,
    isRecording: false,
    audioBlob: null,
    mediaRecorder: null,
    audioChunks: [],
    recognizedText: '',
    translatedText: '',
    isProcessing: false,
    recognition: null,
    useWebSpeechAPI: true  // Use browser's Web Speech API for real transcription
};

// ===================================
// DOM Elements
// ===================================
const elements = {
    inputLanguage: document.getElementById('inputLanguage'),
    targetLanguage: document.getElementById('targetLanguage'),
    recordBtn: document.getElementById('recordBtn'),
    stopBtn: document.getElementById('stopBtn'),
    recordingIndicator: document.getElementById('recordingIndicator'),
    transcriptionText: document.getElementById('transcriptionText'),
    translateBtn: document.getElementById('translateBtn'),
    translationText: document.getElementById('translationText'),
    playBtn: document.getElementById('playBtn'),
    statusMessage: document.getElementById('statusMessage'),
    statusText: document.getElementById('statusText')
};

// ===================================
// Initialization
// ===================================
function init() {
    console.log('Initializing Voice Translation App...');
    
    // Check for Web Speech API support
    checkWebSpeechAPISupport();
    
    // Set up event listeners
    setupEventListeners();
    
    console.log('App initialized successfully');
}

function checkWebSpeechAPISupport() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    console.log('Browser:', navigator.userAgent);
    console.log('SpeechRecognition available:', !!SpeechRecognition);
    
    if (SpeechRecognition) {
        console.log('✅ Web Speech API is supported!');
        appState.useWebSpeechAPI = true;
        showStatus('🎤 Real speech recognition enabled! Use Chrome or Edge for best results.', 'success');
        setTimeout(hideStatus, 5000);
    } else {
        console.warn('⚠️ Web Speech API not supported. Using backend transcription.');
        appState.useWebSpeechAPI = false;
        showStatus('⚠️ Please use Chrome or Edge browser for real speech recognition. Currently using demo mode.', 'info');
        setTimeout(hideStatus, 6000);
    }
}

// ===================================
// Event Listeners
// ===================================
function setupEventListeners() {
    // Language selection
    elements.inputLanguage.addEventListener('change', handleInputLanguageChange);
    elements.targetLanguage.addEventListener('change', handleTargetLanguageChange);
    
    // Recording controls
    elements.recordBtn.addEventListener('click', startRecording);
    elements.stopBtn.addEventListener('click', stopRecording);
    
    // Manual text input
    elements.transcriptionText.addEventListener('input', handleTextInput);
    elements.transcriptionText.addEventListener('keydown', handleTextKeydown);
    
    // Translation
    elements.translateBtn.addEventListener('click', translateText);

    // Playback
    elements.playBtn.addEventListener('click', playTranslation);
}

// ===================================
// Language Selection Handlers
// ===================================
function handleInputLanguageChange(event) {
    appState.inputLanguage = event.target.value;
    console.log('Input language selected:', appState.inputLanguage);
    
    // Enable record button if language is selected
    if (appState.inputLanguage) {
        elements.recordBtn.disabled = false;
        showStatus('Input language selected: ' + getLanguageName(appState.inputLanguage), 'success');
    } else {
        elements.recordBtn.disabled = true;
    }
    
    // Update translate button state since it depends on input language too
    updateTranslateButtonState();
    
    // Hide status after 2 seconds
    setTimeout(hideStatus, 2000);
}

function handleTargetLanguageChange(event) {
    appState.targetLanguage = event.target.value;
    console.log('Target language selected:', appState.targetLanguage);
    
    // Enable translate button if language is selected and text exists
    updateTranslateButtonState();
    
    if (appState.targetLanguage) {
        showStatus('Target language selected: ' + getLanguageName(appState.targetLanguage), 'success');
        setTimeout(hideStatus, 2000);
    }
}

function updateTranslateButtonState() {
    const hasText = appState.recognizedText && appState.recognizedText.trim().length > 0;
    const hasTargetLang = appState.targetLanguage && appState.targetLanguage.length > 0;
    
    // Enable translate button if text and target language are present
    // We don't disable it for inputLanguage so the user can get a clickable error message instead.
    elements.translateBtn.disabled = !(hasText && hasTargetLang);
}

function getLanguageName(code) {
    const languageMap = {
        'en-US': 'English (US)',
        'en': 'English',
        'hi-IN': 'Hindi',
        'hi': 'Hindi',
        'ta-IN': 'Tamil',
        'ta': 'Tamil',
        'te-IN': 'Telugu',
        'te': 'Telugu',
        'kn-IN': 'Kannada',
        'kn': 'Kannada',
        'ml-IN': 'Malayalam',
        'ml': 'Malayalam',
        'bn-IN': 'Bengali',
        'bn': 'Bengali',
        'mr-IN': 'Marathi',
        'mr': 'Marathi',
        'or': 'Odia'
    };
    return languageMap[code] || code;
}

// ===================================
// Audio Recording Functions
// ===================================
async function startRecording() {
    try {
        console.log('Starting speech recognition...');
        
        // Validate input language is selected
        if (!appState.inputLanguage) {
            showStatus('Please select an input language first', 'error');
            return;
        }
        
        // Use Web Speech API if available
        if (appState.useWebSpeechAPI) {
            startWebSpeechRecognition();
        } else {
            // Fallback to audio recording + backend
            startAudioRecording();
        }
        
    } catch (error) {
        console.error('Error starting recording:', error);
        showStatus('Failed to start recording: ' + error.message, 'error');
    }
}

function startWebSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.error('Web Speech API not supported');
        showStatus('⚠️ Web Speech API not available in this browser. Please use Chrome or Edge.', 'error');
        startAudioRecording();
        return;
    }
    
    console.log('Initializing Web Speech Recognition...');
    console.log('Selected language:', appState.inputLanguage);
    
    // Initialize speech recognition
    appState.recognition = new SpeechRecognition();
    
    // Map language codes (remove -IN suffix for Web Speech API)
    const langCode = appState.inputLanguage;
    appState.recognition.lang = langCode;
    
    console.log('Recognition language set to:', langCode);
    
    appState.recognition.continuous = false;
    appState.recognition.interimResults = false;
    appState.recognition.maxAlternatives = 1;
    
    console.log('Recognition settings:', {
        lang: appState.recognition.lang,
        continuous: appState.recognition.continuous,
        interimResults: appState.recognition.interimResults
    });
    
    // Event handlers
    appState.recognition.onstart = () => {
        console.log('🎤 Speech recognition started');
        appState.isRecording = true;
        
        // Update UI
        elements.recordBtn.style.display = 'none';
        elements.stopBtn.style.display = 'inline-flex';
        elements.recordingIndicator.style.display = 'flex';
        elements.inputLanguage.disabled = true;
        
        showStatus('🎤 Listening... Speak now!', 'info');
    };
    
    appState.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const confidence = event.results[0][0].confidence;
        
        console.log('✅ Transcription:', transcript);
        console.log('Confidence:', confidence);
        
        appState.recognizedText = transcript;
        elements.transcriptionText.value = transcript;
        
        showStatus(`✅ Transcription complete! (Confidence: ${(confidence * 100).toFixed(0)}%)`, 'success');
        
        // Update translate button state
        updateTranslateButtonState();
        
        setTimeout(hideStatus, 3000);
    };
    
    appState.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        let errorMessage = 'Speech recognition error: ';
        switch (event.error) {
            case 'no-speech':
                errorMessage += 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage += 'Microphone not found or not working.';
                break;
            case 'not-allowed':
                errorMessage += 'Microphone permission denied.';
                break;
            case 'network':
                errorMessage += 'Network error. Check your connection.';
                break;
            default:
                errorMessage += event.error;
        }
        
        showStatus(errorMessage, 'error');
        resetRecordingUI();
    };
    
    appState.recognition.onend = () => {
        console.log('Speech recognition ended');
        appState.isRecording = false;
        resetRecordingUI();
    };
    
    // Start recognition
    try {
        appState.recognition.start();
    } catch (error) {
        console.error('Failed to start recognition:', error);
        showStatus('Failed to start speech recognition: ' + error.message, 'error');
        resetRecordingUI();
    }
}

async function startAudioRecording() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Initialize MediaRecorder
        appState.mediaRecorder = new MediaRecorder(stream);
        appState.audioChunks = [];
        
        // Set up event handlers
        appState.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                appState.audioChunks.push(event.data);
            }
        };
        
        appState.mediaRecorder.onstop = async () => {
            console.log('Recording stopped, processing audio...');
            
            // Create audio blob
            appState.audioBlob = new Blob(appState.audioChunks, { type: 'audio/webm' });
            console.log('Audio blob created:', appState.audioBlob.size, 'bytes');
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
            
            // Send to backend for transcription
            await transcribeAudio();
        };
        
        // Start recording
        appState.mediaRecorder.start();
        appState.isRecording = true;
        
        // Update UI
        elements.recordBtn.style.display = 'none';
        elements.stopBtn.style.display = 'inline-flex';
        elements.recordingIndicator.style.display = 'flex';
        elements.inputLanguage.disabled = true;
        
        showStatus('Recording... Speak now!', 'info');
        
    } catch (error) {
        console.error('Error starting recording:', error);
        
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            showStatus('Microphone access denied. Please enable microphone permissions.', 'error');
        } else {
            showStatus('Failed to start recording: ' + error.message, 'error');
        }
    }
}

function stopRecording() {
    console.log('Stopping recording...');
    
    // Stop Web Speech API recognition
    if (appState.recognition && appState.isRecording) {
        appState.recognition.stop();
    }
    
    // Stop audio recording
    if (appState.mediaRecorder && appState.isRecording) {
        appState.mediaRecorder.stop();
        appState.isRecording = false;
        
        showStatus('Processing audio...', 'loading');
    }
    
    resetRecordingUI();
}

function resetRecordingUI() {
    // Update UI
    elements.stopBtn.style.display = 'none';
    elements.recordBtn.style.display = 'inline-flex';
    elements.recordingIndicator.style.display = 'none';
    elements.inputLanguage.disabled = false;
}

// ===================================
// Speech-to-Text Functions
// ===================================
async function transcribeAudio() {
    try {
        console.log('Sending audio to backend for transcription...');
        appState.isProcessing = true;
        
        // Create FormData
        const formData = new FormData();
        formData.append('audio', appState.audioBlob, 'recording.webm');
        formData.append('input_language', appState.inputLanguage);
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/stt`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Transcription failed');
        }
        
        if (data.success && data.recognized_text) {
            appState.recognizedText = data.recognized_text;
            elements.transcriptionText.value = data.recognized_text;
            
            console.log('Transcription successful:', data.recognized_text);
            showStatus('Transcription complete!', 'success');
            
            // Update translate button state
            updateTranslateButtonState();
            
            setTimeout(hideStatus, 3000);
        } else {
            throw new Error('No text recognized');
        }
        
    } catch (error) {
        console.error('Transcription error:', error);
        showStatus('Transcription failed: ' + error.message, 'error');
    } finally {
        appState.isProcessing = false;
    }
}

// ===================================
// Translation Functions
// ===================================
async function translateText() {
    try {
        console.log('Translating text...');
        
        // Validate inputs
        if (!appState.recognizedText || appState.recognizedText.trim().length === 0) {
            showStatus('No text to translate. Please record audio first.', 'error');
            return;
        }
        
        if (!appState.targetLanguage) {
            showStatus('Please select a target language.', 'error');
            return;
        }

        if (!appState.inputLanguage) {
            showStatus('Please select an input (spoken) language so we know what language the text is in.', 'error');
            return;
        }
        
        appState.isProcessing = true;
        showStatus('Translating...', 'loading');
        
        // Determine source language (remove -IN suffix if present)
        const sourceLanguage = appState.inputLanguage.replace('-IN', '').toLowerCase();
        
        // Prepare request
        const requestBody = {
            text: appState.recognizedText,
            source_language: sourceLanguage === 'en-us' ? 'en' : sourceLanguage,
            target_language: appState.targetLanguage
        };
        
        console.log('Translation request:', requestBody);
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Translation failed');
        }
        
        if (data.success && data.translated_text) {
            appState.translatedText = data.translated_text;
            elements.translationText.value = data.translated_text;
            elements.playBtn.disabled = false;
            
            console.log('Translation successful:', data.translated_text);
            showStatus('Translation complete!', 'success');
            
            setTimeout(hideStatus, 3000);
        } else {
            throw new Error('Translation returned empty result');
        }
        
    } catch (error) {
        console.error('Translation error:', error);
        showStatus('Translation failed: ' + error.message, 'error');
    } finally {
        appState.isProcessing = false;
    }
}

// ===================================
// UI Helper Functions
// ===================================
function showStatus(message, type = 'info') {
    elements.statusText.textContent = message;
    elements.statusMessage.className = `status-message ${type}`;
    elements.statusMessage.style.display = 'block';
}

function hideStatus() {
    elements.statusMessage.style.display = 'none';
}

// ===================================
// Event Handlers for Text & TTS
// ===================================
function handleTextInput(event) {
    appState.recognizedText = event.target.value;
    updateTranslateButtonState();
}

function handleTextKeydown(event) {
    // Check if Enter was pressed without Shift
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault(); // Prevent adding a new line
        if (!elements.translateBtn.disabled) {
            elements.translateBtn.click();
        } else {
            // Provide a hint why it didn't work
            if (!appState.inputLanguage) {
                showStatus('Please select an input language first.', 'error');
            } else if (!appState.targetLanguage) {
                showStatus('Please select a target language first.', 'error');
            }
        }
    }
}

async function playTranslation() {
    if (!appState.translatedText || !appState.targetLanguage) return;

    try {
        elements.playBtn.disabled = true;
        showStatus('Generating voice. Powered by AI4Bharat Indic-TTS...', 'loading');

        const requestBody = {
            text: appState.translatedText,
            target_language: appState.targetLanguage
        };

        const response = await fetch(`${API_BASE_URL}/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Voice generation failed on server');
        }

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        
        const audio = new Audio(audioUrl);
        
        audio.oncanplay = () => {
            showStatus('Playing translation loudly...', 'info');
            audio.play();
        };

        audio.onended = () => {
            elements.playBtn.disabled = false;
            setTimeout(hideStatus, 2000);
            URL.revokeObjectURL(audioUrl);
        };

        audio.onerror = (e) => {
            console.error('Audio playback error:', e);
            elements.playBtn.disabled = false;
            showStatus('Error playing generated audio.', 'error');
            URL.revokeObjectURL(audioUrl);
        };

    } catch (error) {
        console.error('TTS error:', error);
        elements.playBtn.disabled = false;
        showStatus('Failed to generate voice: ' + error.message, 'error');
    }
}

// ===================================
// Initialize App on Page Load
// ===================================
document.addEventListener('DOMContentLoaded', init);
