import React from 'react';
import { User, Shield, GraduationCap, Users, BookOpen, Crown, Globe, LogOut } from 'lucide-react';

export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिन्दी (Hindi)' },
  { code: 'ta', label: 'தமிழ் (Tamil)' },
  { code: 'te', label: 'తెలుగు (Telugu)' },
  { code: 'mr', label: 'मराठी (Marathi)' },
  { code: 'bn', label: 'বাংলা (Bengali)' },
  { code: 'gu', label: 'ગુજરાતી (Gujarati)' },
  { code: 'pa', label: 'ਪੰਜਾਬੀ (Punjabi)' },
  { code: 'kn', label: 'ಕನ್ನಡ (Kannada)' },
  { code: 'ml', label: 'മലയാളം (Malayalam)' },
  { code: 'ur', label: 'اردو (Urdu)' }
];

export default function Navbar({ activeRole, setRole, currentUser, selectedLanguage, setLanguage, onLogout }) {
  const roles = [
    { id: 'STUDENT', label: 'Student', icon: GraduationCap },
    { id: 'PARENT', label: 'Parent', icon: Users },
    { id: 'TEACHER', label: 'Teacher', icon: BookOpen },
    { id: 'PRINCIPAL', label: 'Principal', icon: Crown },
  ];

  return (
    <header className="navbar">
      <div className="brand-container">
        <div className="brand-logo">P</div>
        <div>
          <h1 className="brand-title">PARTH ASSISTANT AI</h1>
          <span style={{ fontSize: '0.7rem', color: '#94a3b8', letterSpacing: '0.5px' }}>
            SCHOOL ERP AI ECOSYSTEM
          </span>
        </div>
      </div>

      <div className="role-switcher-bar">
        {roles.map((r) => {
          const Icon = r.icon;
          const isActive = activeRole === r.id;
          return (
            <button
              key={r.id}
              className={`role-btn ${r.id} ${isActive ? 'active' : ''}`}
              onClick={() => setRole(r.id)}
            >
              <Icon size={16} />
              {r.label}
            </button>
          );
        })}
      </div>

      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        {/* Multilingual Selector Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'var(--bg-card)', padding: '0.4rem 0.8rem', borderRadius: '20px', border: '1px solid var(--border-color)' }}>
          <Globe size={16} color="#60a5fa" />
          <select
            value={selectedLanguage}
            onChange={(e) => setLanguage(e.target.value)}
            style={{ background: 'transparent', border: 'none', color: 'white', fontSize: '0.8rem', outline: 'none', cursor: 'pointer' }}
          >
            {LANGUAGES.map(l => (
              <option key={l.code} value={l.code} style={{ background: '#0f172a', color: 'white' }}>
                {l.label}
              </option>
            ))}
          </select>
        </div>

        <div className="user-profile-badge">
          <div className="user-avatar">{currentUser.name ? currentUser.name.charAt(0) : 'U'}</div>
          <div className="user-info">
            <span className="user-name">{currentUser.name}</span>
            <span className="user-role-label">{activeRole}</span>
          </div>

          {onLogout && (
            <button
              onClick={onLogout}
              title="Logout"
              className="logout-icon-btn"
              style={{ background: 'transparent', border: 'none', color: '#f87171', cursor: 'pointer', marginLeft: '0.5rem', display: 'flex', alignItems: 'center' }}
            >
              <LogOut size={16} />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}

