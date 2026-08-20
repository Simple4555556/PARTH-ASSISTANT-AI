import React from 'react';
import { Crown, Users, TrendingUp, Sparkles, Building, AlertTriangle } from 'lucide-react';

export default function PrincipalDashboard({ onOpenAI }) {
  const analytics = {
    overallAttendance: 92.4,
    totalStudents: 1250,
    presentToday: 1155,
    absentToday: 75,
    onLeaveToday: 20,
    classWise: [
      { name: "Grade 10-A", rate: 93.5, total: 38 },
      { name: "Grade 10-B", rate: 91.0, total: 40 },
      { name: "Grade 9-A", rate: 94.2, total: 36 },
      { name: "Grade 9-B", rate: 90.8, total: 35 },
      { name: "Grade 8-A", rate: 92.6, total: 42 }
    ],
    monthlyTrends: [
      { month: "April", rate: 94.5 },
      { month: "May", rate: 93.8 },
      { month: "June", rate: 91.2 },
      { month: "July", rate: 92.0 },
      { month: "August (Current)", rate: 92.4 }
    ]
  };

  return (
    <div className="dashboard-content">
      <div className="dashboard-header">
        <div>
          <h2 className="dashboard-title">School Management & Executive Portal</h2>
          <p className="dashboard-subtitle">Principal: <strong>Dr. V. K. Raman</strong> | Campus Operational Intelligence</p>
        </div>
        <button className="pill-btn" style={{ background: 'var(--role-principal)', border: 'none', padding: '0.6rem 1.2rem', display: 'flex', gap: '0.5rem', alignItems: 'center', color: 'white' }} onClick={onOpenAI}>
          <Sparkles size={16} /> Management AI Assistant
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-title">OVERALL SCHOOL ATTENDANCE</span>
          <div className="stat-value" style={{ color: '#c084fc' }}>{analytics.overallAttendance}%</div>
          <div className="stat-subtext" style={{ color: '#c084fc' }}>
            <TrendingUp size={14} /> +0.4% vs last month average
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">TOTAL ENROLLED STUDENTS</span>
          <div className="stat-value">{analytics.totalStudents}</div>
          <div className="stat-subtext" style={{ color: '#94a3b8' }}>
            Across 32 Sections
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">PRESENT TODAY</span>
          <div className="stat-value" style={{ color: '#34d399' }}>{analytics.presentToday}</div>
          <div className="stat-subtext" style={{ color: '#34d399' }}>
            {analytics.absentToday} Absentees | {analytics.onLeaveToday} On Leave
          </div>
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Class-Wise Attendance Distribution</h3>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {analytics.classWise.map((c, i) => (
            <div key={i}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.85rem' }}>
                <span style={{ fontWeight: 600 }}>{c.name} ({c.total} students)</span>
                <span style={{ fontWeight: 700, color: c.rate >= 93 ? '#34d399' : '#fbbf24' }}>{c.rate}%</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '6px', height: '10px', overflow: 'hidden' }}>
                <div style={{ width: `${c.rate}%`, background: 'var(--ai-glow-gradient)', height: '100%', borderRadius: '6px' }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Monthly Attendance Performance Trends</h3>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          {analytics.monthlyTrends.map((m, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid var(--border-color)' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{m.month}</span>
              <h4 style={{ fontSize: '1.4rem', fontWeight: 800, marginTop: '0.25rem', color: '#60a5fa' }}>{m.rate}%</h4>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
