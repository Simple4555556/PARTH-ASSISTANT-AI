import React, { useState } from 'react';
import { CheckCircle, XCircle, Clock, Sparkles, BookOpen } from 'lucide-react';

export default function TeacherDashboard({ onOpenAI, token }) {
  const [students, setStudents] = useState([
    { id: "S101", name: "Aarav Sharma", roll: 14, class: "10-A", status: "PRESENT" },
    { id: "S102", name: "Ananya Patel", roll: 15, class: "10-A", status: "PRESENT" },
    { id: "S103", name: "Rohan Gupta", roll: 16, class: "9-B", status: "PRESENT" }
  ]);
  const [notification, setNotification] = useState(null);

  const toggleStatus = (id) => {
    setStudents(prev => prev.map(s => {
      if (s.id === id) {
        const nextStatus = s.status === "PRESENT" ? "ABSENT" : "PRESENT";
        return { ...s, status: nextStatus };
      }
      return s;
    }));
  };

  const handleMarkAttendance = async () => {
    setNotification("Updating attendance records in School ERP database...");
    setTimeout(() => {
      setNotification("✓ Attendance for Class 10-A successfully recorded and verified!");
    }, 800);
  };

  return (
    <div className="dashboard-content">
      <div className="dashboard-header">
        <div>
          <h2 className="dashboard-title">Teacher Command Center</h2>
          <p className="dashboard-subtitle">Faculty: <strong>Sunita Verma</strong> | Mathematics Dept | Classes: 10-A, 9-B</p>
        </div>
        <button className="pill-btn" style={{ background: 'var(--role-teacher)', border: 'none', padding: '0.6rem 1.2rem', display: 'flex', gap: '0.5rem', alignItems: 'center', color: 'white' }} onClick={onOpenAI}>
          <Sparkles size={16} /> Teaching AI Assistant
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-title">ASSIGNED CLASSES</span>
          <div className="stat-value">2</div>
          <div className="stat-subtext" style={{ color: '#93c5fd' }}>
            Grade 10-A (38 students), Grade 9-B (35 students)
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">TODAY'S CLASS ATTENDANCE</span>
          <div className="stat-value">93.5%</div>
          <div className="stat-subtext" style={{ color: '#34d399' }}>
            <CheckCircle size={14} /> 68 / 73 Students Present
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-title">NEXT LECTURE</span>
          <div className="stat-value" style={{ fontSize: '1.5rem' }}>10:30 AM</div>
          <div className="stat-subtext" style={{ color: '#fbbf24' }}>
            <Clock size={14} /> Grade 10-A — Mathematics
          </div>
        </div>
      </div>

      <div className="card-panel">
        <div className="panel-header">
          <h3 className="panel-title">Mark Attendance — Class 10-A (Today: 19 Aug 2026)</h3>
          <button className="pill-btn" style={{ background: 'var(--primary-blue)', border: 'none' }} onClick={handleMarkAttendance}>
            Submit Attendance
          </button>
        </div>

        {notification && (
          <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', color: '#34d399', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.85rem' }}>
            {notification}
          </div>
        )}

        <table className="custom-table">
          <thead>
            <tr>
              <th>Roll</th>
              <th>Student ID</th>
              <th>Student Name</th>
              <th>Class</th>
              <th>Attendance Status</th>
              <th>Toggle Action</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id}>
                <td>{s.roll}</td>
                <td>{s.id}</td>
                <td style={{ fontWeight: 600 }}>{s.name}</td>
                <td>{s.class}</td>
                <td>
                  <span className={`badge ${s.status === 'PRESENT' ? 'badge-success' : 'badge-danger'}`}>
                    {s.status}
                  </span>
                </td>
                <td>
                  <button className="pill-btn" style={{ fontSize: '0.75rem', padding: '0.3rem 0.7rem' }} onClick={() => toggleStatus(s.id)}>
                    Change to {s.status === 'PRESENT' ? 'ABSENT' : 'PRESENT'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
