import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Send, Sparkles, Mic, Keyboard, Globe, RotateCcw, Square, LayoutDashboard } from 'lucide-react';
import VoiceControls, { VOICE_STATES } from './VoiceControls';
import VoiceWaveform from './VoiceWaveform';
import AIAvatar from './AIAvatar';
import { renderRegistryComponent } from './registry/ComponentRegistry';
import StudentDashboard from './StudentDashboard';
import ParentDashboard from './ParentDashboard';
import TeacherDashboard from './TeacherDashboard';
import PrincipalDashboard from './PrincipalDashboard';
import { getUIString } from '../utils/localizedStrings';
import { API_BASE_URL } from '../config/api';

function getPersonaTitle(role) {
  switch (role) {
    case 'STUDENT': return 'Academic Assistant';
    case 'PARENT': return 'Parent Support Assistant';
    case 'TEACHER': return 'Teaching Assistant';
    case 'PRINCIPAL': return 'Management Assistant';
    default: return 'School Assistant';
  }
}

const LANG_LOCALE = {
  en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN', te: 'te-IN',
  mr: 'mr-IN', bn: 'bn-IN', gu: 'gu-IN', pa: 'pa-IN',
  kn: 'kn-IN', ml: 'ml-IN', ur: 'ur-IN'
};

export default function ParthAssistantUI({ activeRole, currentUser, token, selectedLanguage, setLanguage }) {
  const [conversationId, setConversationId] = useState(`CONV-${Math.floor(1000 + Math.random() * 9000)}`);
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: getUIString(selectedLanguage, 'greeting'),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      persona: getPersonaTitle(activeRole),
      intent: 'GREETING',
      tool: null,
      isVoice: false
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [toolActivity, setToolActivity] = useState(null);
  const [avatarState, setAvatarState] = useState('IDLE');

  // Dynamic Workspace Component State
  const [activeComponent, setActiveComponent] = useState(null);
  const [componentData, setComponentData] = useState({});

  // Voice state
  const [voiceState, setVoiceState] = useState(VOICE_STATES.IDLE);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [lastTtsText, setLastTtsText] = useState('');
  const utteranceRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isThinking, toolActivity]);

  useEffect(() => {
    const newConvId = `CONV-${Math.floor(1000 + Math.random() * 9000)}`;
    setConversationId(newConvId);
    setMessages([
      {
        sender: 'ai',
        text: getUIString(selectedLanguage, 'greeting'),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        persona: getPersonaTitle(activeRole),
        intent: 'GREETING',
        tool: null,
        isVoice: false
      }
    ]);
    setActiveComponent(null);
    setComponentData({});
    stopSpeech();
  }, [activeRole, currentUser, selectedLanguage]);

  // TTS Voice Synthesis
  const speakText = useCallback((text, lang = 'en') => {
    if (!window.speechSynthesis) return;
    stopSpeech();
    const utterance = new SpeechSynthesisUtterance(text);
    const targetLocale = (LANG_LOCALE[lang] || 'en-IN').toLowerCase();
    utterance.lang = LANG_LOCALE[lang] || 'en-IN';
    utterance.rate = 0.95;
    utterance.pitch = 1;

    // Search available browser voices for exact language match
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find(v =>
      v.lang.toLowerCase().replace('_', '-').startsWith(targetLocale) ||
      v.lang.toLowerCase().includes(lang)
    );

    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    utteranceRef.current = utterance;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setVoiceState(VOICE_STATES.SPEAKING);
      setAvatarState('SPEAKING');
    };
    utterance.onend = () => {
      setIsSpeaking(false);
      setVoiceState(VOICE_STATES.IDLE);
      setAvatarState('IDLE');
    };
    utterance.onerror = () => {
      setIsSpeaking(false);
      setVoiceState(VOICE_STATES.IDLE);
      setAvatarState('IDLE');
    };

    window.speechSynthesis.speak(utterance);
  }, []);

  const stopSpeech = useCallback(() => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setIsSpeaking(false);
    if (voiceState === VOICE_STATES.SPEAKING) setVoiceState(VOICE_STATES.IDLE);
    setAvatarState('IDLE');
  }, [voiceState]);

  const replaySpeech = useCallback(() => {
    if (lastTtsText) speakText(lastTtsText, selectedLanguage);
  }, [lastTtsText, selectedLanguage, speakText]);

  const getQuickPills = (role, lang) => {
    if (lang === 'hi') {
      switch (role) {
        case 'STUDENT': return ['मेरी attendance कितनी है?', 'रीसेंट लॉग्स दिखाओ', 'टाइमटेबल दिखाओ', 'डैशबोर्ड खोलो'];
        case 'PARENT': return ['राहुल की attendance कितनी है?', 'रीसेंट उपस्थित दिखाओ', 'शिक्षक से बात करो', 'डैशबोर्ड खोलो'];
        case 'TEACHER': return ['राहुल को अनुपस्थित दर्ज करो', 'टाइमटेबल दिखाओ', 'डैशबोर्ड खोलो'];
        case 'PRINCIPAL': return ['विद्यालय की कुल उपस्थिति क्या है?', 'डेटाबेस दिखाओ', 'डैशबोर्ड खोलो'];
        default: return ['सहायता', 'उपस्थिति स्थिति'];
      }
    }
    switch (role) {
      case 'STUDENT': return ['What is my attendance?', 'Show recent logs', 'Show timetable', 'Open dashboard'];
      case 'PARENT': return ['Rahul ki attendance kitni hai?', 'Show recent attendance', 'Talk to teacher', 'Open dashboard'];
      case 'TEACHER': return ['Mark Rahul absent today', 'Show timetable', 'Open dashboard'];
      case 'PRINCIPAL': return ['What is overall school attendance?', 'Show me the database', 'Open dashboard'];
      default: return ['Help', 'Attendance status'];
    }
  };

  const handleSendMessage = async (textToSend, isVoiceInput = false) => {
    const query = textToSend || inputText;
    if (!query.trim()) return;

    if (isSpeaking) stopSpeech();

    const userMsg = {
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isVoice: isVoiceInput
    };

    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInputText('');
    setIsThinking(true);
    setAvatarState('THINKING');
    setVoiceState(VOICE_STATES.PROCESSING);
    setToolActivity(getUIString(selectedLanguage, 'analyzing'));

    try {
      const endpoint = isVoiceInput ? `${API_BASE_URL}/api/ai/voice` : `${API_BASE_URL}/api/ai/chat`;
      const body = isVoiceInput
        ? { transcript: query, conversation_id: conversationId, language: selectedLanguage || 'en' }
        : { message: query, conversation_id: conversationId, language: selectedLanguage || 'en' };

      console.log('[Parth AI] Sending to:', endpoint);

      const chatController = new AbortController();
      const chatTimeout = setTimeout(() => chatController.abort(), 30000);

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(body),
        signal: chatController.signal
      });
      clearTimeout(chatTimeout);

      if (response.status === 401) {
        throw new Error("AUTH_EXPIRED");
      } else if (response.status === 403) {
        throw new Error("PERMISSION_DENIED");
      } else if (!response.ok) {
        throw new Error(`SERVER_ERROR_${response.status}`);
      }

      const data = await response.json();

      if (data.tool_used) setToolActivity(`Executed Tool: ${data.tool_used}`);
      else setToolActivity(null);

      const responseText = data.message || data.response || getUIString(selectedLanguage, 'retryText');
      const responseLang = data.language || selectedLanguage || 'en';

      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          {
            sender: 'ai',
            text: responseText,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            persona: data.persona,
            intent: data.intent,
            tool: data.tool_used,
            component: data.component,
            isVoice: isVoiceInput
          }
        ]);
        setIsThinking(false);
        setToolActivity(null);

        // Update Dynamic Workspace Component
        if (data.component && data.ui_action !== 'NONE') {
          setActiveComponent(data.component);
          setComponentData(data.data || {});
        } else if (data.intent === 'OPEN_DASHBOARD' || data.component === 'full-dashboard') {
          setActiveComponent('full-dashboard');
        }

        setLastTtsText(responseText);
        if (isVoiceInput || voiceState !== VOICE_STATES.IDLE) {
          speakText(responseText, responseLang);
        } else {
          setVoiceState(VOICE_STATES.IDLE);
          setAvatarState('IDLE');
        }
      }, 250);

    } catch (err) {
      console.error('[Parth Assistant AI API Connection Error]', { endpoint, errorName: err.name, errorMessage: err.message });
      let errMessage = getUIString(selectedLanguage, 'errorText');
      if (err.name === 'AbortError') {
        errMessage = 'The school service took too long to respond. Please try again.';
      } else if (err.message === 'AUTH_EXPIRED') {
        errMessage = 'Your session has expired. Please log in again.';
      } else if (err.message === 'PERMISSION_DENIED') {
        errMessage = "You don't have permission to access that information.";
      } else if (err.name === 'TypeError' || (err.message && (err.message.includes('fetch') || err.message.includes('SERVER_ERROR')))) {
        errMessage = 'School service is temporarily unavailable. Please start the backend server and try again.';
      }

      setMessages(prev => [
        ...prev,
        {
          sender: 'ai',
          text: errMessage,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          persona: getPersonaTitle(activeRole),
          intent: 'ERROR',
          tool: null,
          isVoice: false
        }
      ]);
      setIsThinking(false);
      setToolActivity(null);
      setVoiceState(VOICE_STATES.IDLE);
      setAvatarState('IDLE');
    }
  };

  const handleVoiceTranscript = (transcript) => {
    setInputText(transcript);
    handleSendMessage(transcript, true);
  };

  const renderFullDashboard = () => {
    switch (activeRole) {
      case 'STUDENT': return <StudentDashboard onOpenAI={() => {}} />;
      case 'PARENT': return <ParentDashboard onOpenAI={() => {}} />;
      case 'TEACHER': return <TeacherDashboard onOpenAI={() => {}} token={token} />;
      case 'PRINCIPAL': return <PrincipalDashboard onOpenAI={() => {}} />;
      default: return null;
    }
  };

  return (
    <div className="conversational-workspace">
      {/* Hero Header Area */}
      <div className="hero-assistant-box animate-fade-in">
        <AIAvatar avatarState={avatarState} />
        <h2 className="hero-title">PARTH ASSISTANT AI</h2>
        <p className="hero-subtitle">"{getUIString(selectedLanguage, 'greeting')}"</p>

        {/* Modality Options Row */}
        <div className="modality-controls-row">
          <div className="modality-badge">
            <Mic size={16} className="text-accent" />
            <span>{getUIString(selectedLanguage, 'speak')}</span>
          </div>
          <div className="modality-badge">
            <Keyboard size={16} className="text-accent" />
            <span>{getUIString(selectedLanguage, 'type')}</span>
          </div>
          <div className="modality-badge">
            <Globe size={16} className="text-accent" />
            <span>{getUIString(selectedLanguage, 'language')} ({selectedLanguage.toUpperCase()})</span>
          </div>
        </div>
      </div>

      {/* Main Workspace Split Grid */}
      <div className="main-workspace-grid">
        {/* Left Side: Conversational Chat Stream */}
        <div className="chat-panel-container">
          <div className="chat-messages-container">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-bubble ${msg.sender}`}>
                <p style={{ whiteSpace: 'pre-line' }}>
                  {msg.isVoice && msg.sender === 'user' && (
                    <span style={{ fontSize: '0.7rem', marginRight: '0.4rem', opacity: 0.7 }}>🎤</span>
                  )}
                  {msg.text}
                </p>
                <div className="message-meta">
                  <span>{msg.time}</span>
                  {msg.intent && <span>• {msg.intent}</span>}
                  {msg.component && <span style={{ color: '#34d399' }}>• UI: {msg.component}</span>}
                </div>
              </div>
            ))}

            {toolActivity && (
              <div style={{ padding: '0.4rem 0.8rem', background: 'rgba(59,130,246,0.15)', border: '1px dashed #3b82f6', borderRadius: '12px', fontSize: '0.75rem', color: '#93c5fd', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <Sparkles size={14} /> {toolActivity}
              </div>
            )}

            {isThinking && !toolActivity && (
              <div className="message-bubble ai" style={{ opacity: 0.8 }}>
                <p style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <Sparkles size={14} /> {getUIString(selectedLanguage, 'thinking')}
                </p>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div style={{ padding: '0.25rem 1rem 0' }}>
            <VoiceWaveform voiceState={voiceState} />
          </div>

          <div className="quick-pills-row">
            {getQuickPills(activeRole, selectedLanguage).map((pill, i) => (
              <button key={i} className="pill-btn" onClick={() => handleSendMessage(pill, false)}>{pill}</button>
            ))}
          </div>

          <div className="chat-input-container">
            <VoiceControls
              voiceState={voiceState}
              setVoiceState={setVoiceState}
              onTranscript={handleVoiceTranscript}
              selectedLanguage={selectedLanguage}
              isSpeaking={isSpeaking}
              onStopSpeech={stopSpeech}
              disabled={isThinking}
            />

            <input
              type="text"
              className="chat-input"
              placeholder={getUIString(selectedLanguage, 'askPlaceholder')}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            />

            <button className="send-btn" onClick={() => handleSendMessage()}>
              <Send size={18} />
            </button>
          </div>
        </div>

        {/* Right Side: Dynamic Contextual Workspace Pane */}
        <div className="dynamic-workspace-pane">
          {activeComponent === 'full-dashboard' ? (
            <div style={{ width: '100%', height: '100%', overflowY: 'auto' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>
                <span style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <LayoutDashboard size={18} className="text-accent" /> {getUIString(selectedLanguage, 'fullDashboard')} ({activeRole})
                </span>
                <button
                  className="pill-btn"
                  onClick={() => setActiveComponent(null)}
                  style={{ fontSize: '0.75rem' }}
                >
                  {getUIString(selectedLanguage, 'closeDashboard')}
                </button>
              </div>
              {renderFullDashboard()}
            </div>
          ) : activeComponent ? (
            renderRegistryComponent(activeComponent, {
              data: componentData,
              token,
              currentUser,
              onConfirmationSuccess: (msg) => {
                setMessages(prev => [
                  ...prev,
                  {
                    sender: 'ai',
                    text: msg,
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    persona: getPersonaTitle(activeRole),
                    intent: 'ACTION_CONFIRMED',
                    tool: 'mock_erp'
                  }
                ]);
              }
            })
          ) : (
            <div className="empty-workspace-placeholder animate-fade-in">
              <Sparkles size={48} className="text-accent" style={{ opacity: 0.5 }} />
              <h3>{getUIString(selectedLanguage, 'dynamicWorkspaceTitle')}</h3>
              <p style={{ maxWidth: '320px', fontSize: '0.9rem' }}>
                {getUIString(selectedLanguage, 'dynamicWorkspaceDesc')}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
