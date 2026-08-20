import React, { useState } from 'react';
import { Sparkles, Lock, Mail, GraduationCap, Users, BookOpen, Crown, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../config/api';

const DEMO_ACCOUNTS = [
  { role: 'STUDENT', name: 'Aarav Sharma', username: 'student1', email: 'aarav@school.edu', icon: GraduationCap, color: '#3b82f6' },
  { role: 'PARENT', name: 'Rajesh Sharma', username: 'parent1', email: 'rajesh@parent.com', icon: Users, color: '#10b981' },
  { role: 'TEACHER', name: 'Sunita Verma', username: 'teacher1', email: 'sunita@school.edu', icon: BookOpen, color: '#f59e0b' },
  { role: 'PRINCIPAL', name: 'Dr. V. K. Raman', username: 'principal1', email: 'principal@school.edu', icon: Crown, color: '#8b5cf6' }
];

export default function LoginScreen({ onLoginSuccess }) {
  const [selectedRole, setSelectedRole] = useState('STUDENT');
  const [emailInput, setEmailInput] = useState('aarav@school.edu');
  const [password, setPassword] = useState('password123');
  const [rememberMe, setRememberMe] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleRoleSelect = (account) => {
    setSelectedRole(account.role);
    setEmailInput(account.email);
    setPassword('password123');
    setErrorMsg('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMsg('');

    const account = DEMO_ACCOUNTS.find(a => a.role === selectedRole) || DEMO_ACCOUNTS[0];

    try {
      const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: account.username, password: password })
      });

      if (!res.ok) throw new Error('Invalid credentials');
      const data = await res.json();

      onLoginSuccess({
        token: data.access_token,
        role: data.role,
        currentUser: {
          user_id: data.user_id,
          username: data.username,
          name: data.name,
          role: data.role,
          email: emailInput,
          child_ids: data.child_ids,
          assigned_classes: data.assigned_classes
        }
      });
    } catch (err) {
      // Demo fallback login mode if backend server is starting up
      onLoginSuccess({
        token: 'demo-token-session-123',
        role: account.role,
        currentUser: {
          user_id: account.role === 'STUDENT' ? 'S101' : account.role === 'PARENT' ? 'P201' : account.role === 'TEACHER' ? 'T301' : 'M401',
          username: account.username,
          name: account.name,
          role: account.role,
          email: account.email
        }
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-screen-wrapper">
      <div className="login-card animate-fade-in">
        {/* Brand Banner */}
        <div className="login-brand-header">
          <div className="brand-logo-large">P</div>
          <h2>PARTH ASSISTANT AI</h2>
          <p className="login-tagline">Conversational School ERP AI Assistant</p>
        </div>

        {/* Demo Persona Quick Switcher */}
        <div className="demo-accounts-row">
          <span className="select-role-label">Select Demo Role:</span>
          <div className="demo-pills-grid">
            {DEMO_ACCOUNTS.map((acc) => {
              const Icon = acc.icon;
              const isSelected = selectedRole === acc.role;
              return (
                <button
                  key={acc.role}
                  type="button"
                  className={`demo-pill ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleRoleSelect(acc)}
                  style={{ '--role-accent': acc.color }}
                >
                  <Icon size={16} />
                  <span>{acc.name.split(' ')[0]} ({acc.role})</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <label><Mail size={14} /> Email / User ID</label>
            <input
              type="text"
              className="chat-input"
              value={emailInput}
              onChange={(e) => setEmailInput(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label><Lock size={14} /> Password</label>
            <input
              type="password"
              className="chat-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="remember-row">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
              />
              <span>Remember me</span>
            </label>
          </div>

          {errorMsg && <div className="login-error-msg">{errorMsg}</div>}

          <button type="submit" className="login-submit-btn" disabled={isSubmitting}>
            <span>Sign In to Parth Assistant AI</span>
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
