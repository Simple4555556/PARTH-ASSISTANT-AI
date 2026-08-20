import React from 'react';
import { Calendar, CheckCircle, Clock, BookOpen, Sparkles } from 'lucide-react';

export default function StudentDashboard({ onOpenAI }) {
  const student = {
    name: "Aarav Sharma",
    grade: "10-A",
    rollNo: 14,
    attendance: 91.2,
    totalDays: 120,
    presentDays: 109,
    absentDays: 8,
    subjects: [
      { name: "Mathematics", percentage: 94.0, teacher: "Sunita Verma" },
      { name: "Science", percentage: 88.5, teacher: "Dr. K. Mehta" },
      { name: "English", percentage: 92.0, teacher: "Pooja Rao" },
      { name: "Social Studies", percentage: 90.0, teacher: "R. S. Kapoor" },
    ],
    logs: [
      { date: "2026-08-19", status: "PRESENT", subject: "Overall" },
      { date: "2026-08-18", status: "PRESENT", subject: "Overall" },
      { date: "2026-08-17", status: "ABSENT", subject: "Mathematics", remark: "Sick leave" },
      { date: "2026-08-16", status: "PRESENT", subject: "Overall" }
    ]
  };

  return (
    <div className="dashboard-content">
      <div className="dashboard-header">
        <div>
          <h2 className="dashboard-title">Welcome back, {student.name}!</h2>
          <p className="dashboard-subtitle">Class {student.grade} | Roll No: {student.rollNo} | Academic Portal</p>
        </div>
        <button className="pill-btn" style={{ background: 'var(--primary-gradient)', border: 'none', padding: '0.6rem 1.2rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }} onClick={onOpenAI}>
          <Sparkles size={16} /> Ask Parth Assistant AI
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-title">OVERALL ATTENDANCE</span>
          <div className="stat-value">{student.attendance}%</div>
          <div className="stat-subtext">
            <CheckCircle size={14} /> Good Standing (Target: 85%)
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">PRESENT DAYS</span>
          <div className="stat-value">{student.presentDays} <span style={{ fontSize: '1rem', color: '#94a3b8' }}>/ {student.totalDays}</span></div>
          <div className="stat-subtext" style={{ color: '#94a3b8' }}>
            <Calendar size={14} /> Total Academic Days
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">ABSENT DAYS</span>
          <div className="stat-value" style={{ color: '#f87171' }}>{student.absentDays}</div>
          <div className="stat-subtext" style={{ color: '#f87171' }}>
            <Clock size={14} /> 3 Leaves Approved
          </div>
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Subject-Wise Attendance Breakdown</h3>
        </div>
        <div className="stats-grid" style={{ marginBottom: 0 }}>
          {student.subjects.map((sub, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600 }}>{sub.name}</span>
                <span style={{ fontWeight: 700, color: sub.percentage >= 90 ? '#34d399' : '#fbbf24' }}>{sub.percentage}%</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Teacher: {sub.teacher}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Recent Attendance Logs</h3>
        </div>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Subject</th>
              <th>Status</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            {student.logs.map((log, i) => (
              <tr key={i}>
                <td>{log.date}</td>
                <td>{log.subject}</td>
                <td>
                  <span className={`badge ${log.status === 'PRESENT' ? 'badge-success' : 'badge-danger'}`}>
                    {log.status}
                  </span>
                </td>
                <td>{log.remark || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
