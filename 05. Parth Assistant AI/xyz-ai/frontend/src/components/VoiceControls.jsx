import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Square, Volume2, VolumeX, Loader2, AlertCircle } from 'lucide-react';

// Language → BCP-47 locale mapping for Web Speech API
const LANG_LOCALE = {
  en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN', te: 'te-IN',
  mr: 'mr-IN', bn: 'bn-IN', gu: 'gu-IN', pa: 'pa-IN',
  kn: 'kn-IN', ml: 'ml-IN', ur: 'ur-IN'
};

export const VOICE_STATES = {
  IDLE: 'IDLE',
  LISTENING: 'LISTENING',
  PROCESSING: 'PROCESSING',
  SPEAKING: 'SPEAKING',
  ERROR: 'ERROR'
};

export default function VoiceControls({
  voiceState,
  setVoiceState,
  onTranscript,
  selectedLanguage = 'en',
  isSpeaking,
  onStopSpeech,
  disabled = false
}) {
  const recognitionRef = useRef(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [hasSpeechAPI, setHasSpeechAPI] = useState(true);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setHasSpeechAPI(false);
    }
  }, []);

  const startListening = () => {
    if (!hasSpeechAPI) {
      setErrorMsg('Voice input is not supported in this browser. Please use text input.');
      setVoiceState(VOICE_STATES.ERROR);
      return;
    }

    setErrorMsg('');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = LANG_LOCALE[selectedLanguage] || 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;

    recognition.onstart = () => {
      setVoiceState(VOICE_STATES.LISTENING);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setVoiceState(VOICE_STATES.PROCESSING);
      onTranscript(transcript);
    };

    recognition.onerror = (event) => {
      if (event.error === 'not-allowed') {
        setErrorMsg('Microphone permission denied. Please allow microphone access.');
      } else if (event.error === 'no-speech') {
        setErrorMsg('No speech was detected. Please try again.');
      } else if (event.error === 'network') {
        setErrorMsg("Network error. You can continue using text input.");
      } else {
        setErrorMsg(`Voice error: ${event.error}. Please try again.`);
      }
      setVoiceState(VOICE_STATES.ERROR);
    };

    recognition.onend = () => {
      if (voiceState === VOICE_STATES.LISTENING) {
        setVoiceState(VOICE_STATES.IDLE);
      }
    };

    try {
      recognition.start();
    } catch (err) {
      setErrorMsg("Couldn't access voice input right now. You can continue using chat.");
      setVoiceState(VOICE_STATES.ERROR);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setVoiceState(VOICE_STATES.IDLE);
  };

  const handleMicClick = () => {
    if (voiceState === VOICE_STATES.SPEAKING) {
      onStopSpeech();
      return;
    }
    if (voiceState === VOICE_STATES.LISTENING) {
      stopListening();
      return;
    }
    if (voiceState === VOICE_STATES.IDLE || voiceState === VOICE_STATES.ERROR) {
      startListening();
    }
  };

  const getMicButtonStyle = () => {
    const base = {
      width: 56, height: 56, borderRadius: '50%', border: 'none',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all 0.2s ease', position: 'relative', flexShrink: 0
    };
    switch (voiceState) {
      case VOICE_STATES.LISTENING:
        return { ...base, background: 'linear-gradient(135deg, #ef4444, #dc2626)', boxShadow: '0 0 0 0 rgba(239,68,68,0.4)', animation: 'micPulse 1.5s infinite' };
      case VOICE_STATES.PROCESSING:
        return { ...base, background: 'linear-gradient(135deg, #f59e0b, #d97706)' };
      case VOICE_STATES.SPEAKING:
        return { ...base, background: 'linear-gradient(135deg, #22c55e, #16a34a)', boxShadow: '0 0 20px rgba(34,197,94,0.4)' };
      case VOICE_STATES.ERROR:
        return { ...base, background: 'linear-gradient(135deg, #6b7280, #4b5563)' };
      default:
        return { ...base, background: 'linear-gradient(135deg, #3b82f6, #2563eb)', boxShadow: '0 4px 14px rgba(59,130,246,0.4)' };
    }
  };

  const getMicIcon = () => {
    if (voiceState === VOICE_STATES.LISTENING) return <MicOff size={22} color="white" />;
    if (voiceState === VOICE_STATES.PROCESSING) return <Loader2 size={22} color="white" style={{ animation: 'spin 1s linear infinite' }} />;
    if (voiceState === VOICE_STATES.SPEAKING) return <Square size={22} color="white" />;
    if (voiceState === VOICE_STATES.ERROR) return <Mic size={22} color="white" />;
    return <Mic size={22} color="white" />;
  };

  const getStatusLabel = () => {
    switch (voiceState) {
      case VOICE_STATES.LISTENING: return '🔴 Listening...';
      case VOICE_STATES.PROCESSING: return '⏳ Processing...';
      case VOICE_STATES.SPEAKING: return '🔊 Speaking... (tap to stop)';
      case VOICE_STATES.ERROR: return 'Try again';
      default: return hasSpeechAPI ? 'Tap to speak' : 'Voice unavailable';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem' }}>
      <button
        onClick={handleMicClick}
        disabled={disabled || voiceState === VOICE_STATES.PROCESSING}
        style={getMicButtonStyle()}
        aria-label="Talk to Parth Assistant AI"
        title="Talk to Parth Assistant AI"
      >
        {getMicIcon()}
      </button>

      <span style={{ fontSize: '0.65rem', color: '#94a3b8', textAlign: 'center', whiteSpace: 'nowrap' }}>
        {getStatusLabel()}
      </span>

      {errorMsg && voiceState === VOICE_STATES.ERROR && (
        <div style={{
          display: 'flex', alignItems: 'flex-start', gap: '0.3rem',
          background: 'rgba(239,68,68,0.12)', border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: 8, padding: '0.5rem 0.7rem', maxWidth: 220, marginTop: 4
        }}>
          <AlertCircle size={14} color="#f87171" style={{ flexShrink: 0, marginTop: 1 }} />
          <span style={{ fontSize: '0.7rem', color: '#f87171', lineHeight: 1.4 }}>{errorMsg}</span>
        </div>
      )}

      <style>{`
        @keyframes micPulse {
          0% { box-shadow: 0 0 0 0 rgba(239,68,68,0.6); }
          70% { box-shadow: 0 0 0 12px rgba(239,68,68,0); }
          100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
