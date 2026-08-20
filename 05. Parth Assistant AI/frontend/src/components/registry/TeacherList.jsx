import React from 'react';
import { UserCheck, Mail } from 'lucide-react';

export default function TeacherList({ data = {} }) {
  const teachers = data.teachers || [
    { name: 'Sunita Verma', subject: 'Science & Class Teacher', email: 'sunita@school.edu' },
    { name: 'Ramesh Kumar', subject: 'Mathematics', email: 'ramesh@school.edu' },
    { name: 'Ananya Roy', subject: 'English', email: 'ananya@school.edu' }
  ];

  return (
    <div className="context-card teacher-list-card animate-fade-in">
      <div className="card-header-badge">
        <UserCheck size={18} className="text-accent" />
        <span>Assigned Teachers</span>
      </div>

      <div className="teacher-grid">
        {teachers.map((t, i) => (
          <div key={i} className="teacher-card-item">
            <div className="teacher-avatar">{t.name[0]}</div>
            <div className="teacher-details">
              <span className="t-name">{t.name}</span>
              <span className="t-sub">{t.subject}</span>
              <span className="t-email"><Mail size={12} /> {t.email}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
