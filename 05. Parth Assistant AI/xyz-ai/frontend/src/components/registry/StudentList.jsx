import React from 'react';
import { Users } from 'lucide-react';

export default function StudentList({ data = {} }) {
  const students = data.students || [
    { id: 'S101', name: 'Aarav Sharma / Rahul', grade: 'Class 10-A', attendance: '91.2%' },
    { id: 'S102', name: 'Diya Patel', grade: 'Class 10-A', attendance: '95.0%' },
    { id: 'S103', name: 'Kabir Singh', grade: 'Class 10-B', attendance: '88.5%' }
  ];

  return (
    <div className="context-card student-list-card animate-fade-in">
      <div className="card-header-badge">
        <Users size={18} className="text-accent" />
        <span>Student Directory</span>
      </div>

      <div className="student-table">
        <div className="table-row header">
          <span>ID</span>
          <span>Name</span>
          <span>Grade</span>
          <span>Attendance</span>
        </div>
        {students.map((s) => (
          <div key={s.id} className="table-row">
            <span className="sid">{s.id}</span>
            <span className="sname">{s.name}</span>
            <span className="sgrade">{s.grade}</span>
            <span className="satt">{s.attendance}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
