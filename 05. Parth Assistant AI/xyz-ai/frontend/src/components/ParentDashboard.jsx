import React, { useState } from 'react';
import { PhoneCall, CheckCircle, AlertCircle, Sparkles, User } from 'lucide-react';

export default function ParentDashboard({ onOpenAI }) {
  const [callSubmitted, setCallSubmitted] = useState(false);

  const child = {
    name: "Aarav (Rahul) Sharma",
    grade: "10-A",
    attendance: 91.2,
    lastMonthAttendance: 89.5,
    presentDays: 109,
    totalDays: 120,
    classTeacher: "Sunita Verma",
    teacherPhone: "+91-0000000001",
    subject: "Mathematics"

  };

  const handleCallRequest = () => {
    setCallSubmitted(true);
  };

  return (
    <div className="dashboard-content">
      <div className="dashboard-header">
        <div>
          <h2 className="dashboard-title">Parent Support Portal</h2>
          <p className="dashboard-subtitle">Monitoring Progress for: <strong>{child.name} (Grade {child.grade})</strong></p>
        </div>
        <button className="pill-btn" style={{ background: 'var(--role-parent)', border: 'none', padding: '0.6rem 1.2rem', display: 'flex', gap: '0.5rem', alignItems: 'center', color: 'white' }} onClick={onOpenAI}>
          <Sparkles size={16} /> Parent AI Assistant
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-title">CHILD'S ATTENDANCE</span>
          <div className="stat-value">{child.attendance}%</div>
          <div className="stat-subtext" style={{ color: '#34d399' }}>
            <CheckCircle size={14} /> +1.7% increase from last month ({child.lastMonthAttendance}%)
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">CLASSES ATTENDED</span>
          <div className="stat-value">{child.presentDays} <span style={{ fontSize: '1rem', color: '#94a3b8' }}>/ {child.totalDays}</span></div>
          <div className="stat-subtext" style={{ color: '#94a3b8' }}>
            Current Term Record
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">CLASS TEACHER</span>
          <div className="stat-value" style={{ fontSize: '1.5rem' }}>{child.classTeacher}</div>
          <div className="stat-subtext" style={{ color: '#93c5fd' }}>
            {child.subject} Department
          </div>
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Direct Escalation & Teacher Contact</h3>
        </div>
        <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h4 style={{ fontSize: '1rem', fontWeight: 600 }}>Request Call / Meeting with {child.classTeacher}</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Need to discuss {child.name}'s attendance or performance? Submit an automated request.</p>
          </div>
          {callSubmitted ? (
            <span className="badge badge-success" style={{ padding: '0.6rem 1rem', fontSize: '0.85rem' }}>
              ✓ Request REQ-1001 Submitted
            </span>
          ) : (
            <button className="pill-btn" style={{ background: 'var(--primary-blue)', padding: '0.6rem 1.2rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }} onClick={handleCallRequest}>
              <PhoneCall size={16} /> Request Call
            </button>
          )}
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Recent School Notices for Parents</h3>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ padding: '0.9rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', borderLeft: '4px solid #3b82f6' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Aug 19, 2026</span>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 600 }}>Mid-Term Assessment Schedule Released</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Mathematics assessment starts next Monday. Ensure regular class attendance.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
