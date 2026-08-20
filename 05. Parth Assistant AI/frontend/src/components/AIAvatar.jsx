import React from 'react';
import { Sparkles, Mic, Volume2, AlertCircle } from 'lucide-react';

export default function AIAvatar({ avatarState = 'IDLE' }) {
  // avatarState: IDLE | LISTENING | THINKING | SPEAKING | ERROR

  return (
    <div className={`ai-avatar-container state-${avatarState.toLowerCase()}`}>
      <div className="avatar-outer-glow">
        <div className="avatar-core-circle">
          <span className="avatar-letter">P</span>

          {avatarState === 'LISTENING' && (
            <div className="state-overlay listening">
              <Mic size={24} className="mic-icon-pulse" />
              <div className="sound-wave-rings" />
            </div>
          )}

          {avatarState === 'THINKING' && (
            <div className="state-overlay thinking">
              <Sparkles size={24} className="sparkle-spin" />
              <div className="orbit-spinner" />
            </div>
          )}

          {avatarState === 'SPEAKING' && (
            <div className="state-overlay speaking">
              <Volume2 size={24} className="speaker-wave" />
              <div className="equalizer-bars">
                <span className="eq-bar bar1" />
                <span className="eq-bar bar2" />
                <span className="eq-bar bar3" />
              </div>
            </div>
          )}

          {avatarState === 'ERROR' && (
            <div className="state-overlay error">
              <AlertCircle size={24} className="text-danger" />
            </div>
          )}
        </div>
      </div>

      <div className="avatar-state-label">
        <span className={`state-dot ${avatarState.toLowerCase()}`}>●</span>
        <span className="state-text">{avatarState}</span>
      </div>
    </div>
  );
}
