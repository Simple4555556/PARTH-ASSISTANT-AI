import React from 'react';
import { Bell } from 'lucide-react';

export default function NoticeList({ data = {} }) {
  const notices = data.notices || [
    { title: 'Independence Day Holiday', date: 'Aug 15, 2026', desc: 'School remains closed.' },
    { title: 'Term 1 Mid-Examinations Schedule', date: 'Aug 25, 2026', desc: 'Schedules posted for classes 9 to 12.' }
  ];

  return (
    <div className="context-card notice-list-card animate-fade-in">
      <div className="card-header-badge">
        <Bell size={18} className="text-accent" />
        <span>School Notices</span>
      </div>

      <div className="notice-items">
        {notices.map((n, i) => (
          <div key={i} className="notice-item">
            <div className="n-header">
              <span className="n-title">{n.title}</span>
              <span className="n-date">{n.date}</span>
            </div>
            <p className="n-desc">{n.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
