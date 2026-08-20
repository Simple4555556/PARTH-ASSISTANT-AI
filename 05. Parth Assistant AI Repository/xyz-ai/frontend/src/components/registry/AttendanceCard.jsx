import React from 'react';
import { Calendar, CheckCircle2, XCircle, Clock } from 'lucide-react';

export default function AttendanceCard({ data = {} }) {
  const studentName = data.student_name || 'Student';
  const pct = data.overall_percentage ?? 87.5;
  const present = data.present_days ?? 35;
  const absent = data.absent_days ?? 5;
  const total = data.total_days ?? (present + absent);

  return (
    <div className="context-card attendance-card animate-fade-in">
      <div className="card-header-badge">
        <Calendar size={18} className="text-accent" />
        <span>{studentName}'s Attendance</span>
      </div>

      <div className="attendance-percentage-display">
        <div className="percentage-circle">
          <span className="percentage-val">{pct}%</span>
          <span className="percentage-label">Overall</span>
        </div>

        <div className="attendance-stats-grid">
          <div className="stat-pill present">
            <CheckCircle2 size={16} />
            <div>
              <span className="stat-num">{present}</span>
              <span className="stat-desc">Present</span>
            </div>
          </div>
          <div className="stat-pill absent">
            <XCircle size={16} />
            <div>
              <span className="stat-num">{absent}</span>
              <span className="stat-desc">Absent</span>
            </div>
          </div>
          <div className="stat-pill total">
            <Clock size={16} />
            <div>
              <span className="stat-num">{total}</span>
              <span className="stat-desc">Total Days</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
