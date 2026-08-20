import React from 'react';
import { History, Check, X } from 'lucide-react';

export default function RecentAttendance({ data = {} }) {
  const studentName = data.student_name || 'Rahul';
  const logs = data.recent_logs || [
    { date: 'Aug 20', subject: 'Mathematics', status: 'PRESENT' },
    { date: 'Aug 19', subject: 'Science', status: 'PRESENT' },
    { date: 'Aug 18', subject: 'English', status: 'ABSENT' },
    { date: 'Aug 17', subject: 'Computer', status: 'PRESENT' }
  ];

  return (
    <div className="context-card recent-attendance animate-fade-in">
      <div className="card-header-badge">
        <History size={18} className="text-accent" />
        <span>{studentName} — Recent Attendance</span>
      </div>

      <div className="recent-logs-list">
        {logs.map((log, idx) => {
          const isPresent = (log.status || '').toUpperCase() === 'PRESENT';
          return (
            <div key={idx} className={`log-row ${isPresent ? 'is-present' : 'is-absent'}`}>
              <span className="log-date">{log.date}</span>
              <span className="log-subject">{log.subject || 'Overall'}</span>
              <span className={`status-badge ${isPresent ? 'present' : 'absent'}`}>
                {isPresent ? <Check size={14} /> : <X size={14} />}
                {log.status}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
