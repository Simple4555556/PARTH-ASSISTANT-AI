import React, { useState } from 'react';
import { Database, Search, UserCheck } from 'lucide-react';

export default function StudentDatabase({ data = {} }) {
  const [searchQuery, setSearchQuery] = useState('');

  const studentList = data.students || [
    { id: 'STU001', name: 'Rahul Sharma', grade: '10-A', attendance: 91.2, status: 'Active' },
    { id: 'STU002', name: 'Aman Verma', grade: '10-B', attendance: 86.4, status: 'Active' },
    { id: 'STU003', name: 'Priya Patel', grade: '10-A', attendance: 94.1, status: 'Active' },
    { id: 'STU004', name: 'Karan Singh', grade: '9-A', attendance: 88.0, status: 'Active' },
    { id: 'STU005', name: 'Ananya Roy', grade: '9-B', attendance: 92.5, status: 'Active' }
  ];

  const filteredStudents = studentList.filter(s =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.grade.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="context-card student-database-card animate-fade-in">
      <div className="card-header-badge">
        <Database size={18} className="text-accent" />
        <span>Student Academic Database</span>
        <span className="auth-secured-badge">Teacher View</span>
      </div>

      <div className="db-search-bar" style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(0,0,0,0.2)', padding: '0.5rem 0.75rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
        <Search size={16} className="text-accent" />
        <input
          type="text"
          placeholder="Search students by name, ID, or class..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ background: 'transparent', border: 'none', color: 'white', width: '100%', outline: 'none', fontSize: '0.85rem' }}
        />
      </div>

      <div className="student-table" style={{ width: '100%' }}>
        <div className="table-row header">
          <span>ID</span>
          <span>Name</span>
          <span>Class</span>
          <span>Attendance</span>
        </div>
        {filteredStudents.map((s) => (
          <div key={s.id} className="table-row">
            <span className="sid">{s.id}</span>
            <span className="sname">{s.name}</span>
            <span className="sgrade">{s.grade}</span>
            <span className={`satt ${s.attendance >= 90 ? 'text-success' : 'text-danger'}`}>{s.attendance}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
