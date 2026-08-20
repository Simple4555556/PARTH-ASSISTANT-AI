import React from 'react';
import { Clock, BookOpen } from 'lucide-react';

export default function TimetableCard({ data = {} }) {
  const gradeSection = data.grade_section || 'Class 10-A';
  const schedule = data.schedule || [
    { period: 'Period 1 (08:30 - 09:15)', subject: 'Mathematics', teacher: 'Mr. Sharma' },
    { period: 'Period 2 (09:15 - 10:00)', subject: 'Science', teacher: 'Mrs. Sunita' },
    { period: 'Period 3 (10:15 - 11:00)', subject: 'English', teacher: 'Ms. Ananya' },
    { period: 'Period 4 (11:00 - 11:45)', subject: 'Computer Science', teacher: 'Mr. Verma' }
  ];

  return (
    <div className="context-card timetable-card animate-fade-in">
      <div className="card-header-badge">
        <Clock size={18} className="text-accent" />
        <span>{gradeSection} Timetable</span>
      </div>

      <div className="timetable-list">
        {schedule.map((item, idx) => (
          <div key={idx} className="timetable-item">
            <div className="period-time">{item.period}</div>
            <div className="subject-info">
              <BookOpen size={14} className="text-accent" />
              <span className="subject-name">{item.subject}</span>
            </div>
            <div className="teacher-name">{item.teacher}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
