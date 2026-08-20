import React, { useState } from 'react';
import { BarChart3, Users, CheckCircle, XCircle } from 'lucide-react';

export default function AttendanceAnalytics({ data = {} }) {
  const [showBreakdown, setShowBreakdown] = useState(false);

  const overall = data.overall_attendance ?? 88.7;
  const present = data.present_today ?? 4320;
  const absent = data.absent_today ?? 550;
  const classWise = data.class_wise || {
    '10-A': 93.5,
    '10-B': 89.2,
    '9-A': 86.4,
    '9-B': 91.0
  };

  return (
    <div className="context-card analytics-card animate-fade-in">
      <div className="card-header-badge">
        <BarChart3 size={18} className="text-accent" />
        <span>School Attendance</span>
      </div>

      <div className="analytics-body">
        <div className="main-metric">
          <span className="metric-val">{overall}%</span>
          <span className="metric-lbl">Overall School Average</span>
        </div>

        <div className="analytics-counts-row">
          <div className="count-box present">
            <CheckCircle size={16} />
            <div>
              <span className="count-num">{present.toLocaleString()}</span>
              <span className="count-lbl">Present</span>
            </div>
          </div>
          <div className="count-box absent">
            <XCircle size={16} />
            <div>
              <span className="count-num">{absent.toLocaleString()}</span>
              <span className="count-lbl">Absent</span>
            </div>
          </div>
        </div>

        <button
          className="action-link-btn"
          onClick={() => setShowBreakdown(!showBreakdown)}
        >
          {showBreakdown ? 'Hide Class Breakdown' : 'View Class Breakdown'}
        </button>

        {showBreakdown && (
          <div className="class-breakdown-table animate-fade-in">
            <h4>Class Breakdown</h4>
            {Object.entries(classWise).map(([cls, val]) => (
              <div key={cls} className="breakdown-row">
                <span>Class {cls}</span>
                <div className="progress-bar-bg">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${val}%` }}
                  />
                </div>
                <span className="breakdown-val">{val}%</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
