import React, { useState } from 'react';
import { UserCheck, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react';
import { API_BASE_URL } from '../../config/api';

export default function AttendanceForm({ data = {}, token, onConfirmationSuccess }) {
  const studentName = data.student_name || 'Rahul';
  const studentId = data.student_id || 'S101';
  const date = data.date || 'Today';
  const initialStatus = (data.status || 'ABSENT').toUpperCase();

  const [status, setStatus] = useState(initialStatus);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [resultMsg, setResultMsg] = useState(data.confirmed ? `${studentName} has been marked ${initialStatus.toLowerCase()} today.` : null);
  const [isError, setIsError] = useState(false);

  const handleConfirm = async () => {
    setIsSubmitting(true);
    setIsError(false);

    try {
      const todayStr = new Date().toISOString().split('T')[0];
      const res = await fetch(`${API_BASE_URL}/api/mock/attendance/mark`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          student_id: studentId,
          date: todayStr,
          status: status,
          remarks: `Marked by Teacher via Parth Assistant AI`
        })
      });

      if (!res.ok) throw new Error('API failed');
      const resData = await res.json();
      setResultMsg(`${studentName} has been marked ${status.toLowerCase()} today.`);
      if (onConfirmationSuccess) onConfirmationSuccess(`${studentName} has been marked ${status.toLowerCase()} today.`);
    } catch (err) {
      setIsError(true);
      setResultMsg('Attendance could not be updated.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="context-card attendance-form-card animate-fade-in">
      <div className="card-header-badge">
        <UserCheck size={18} className="text-accent" />
        <span>Mark Attendance</span>
      </div>

      <div className="form-body">
        <div className="form-field">
          <label>Student:</label>
          <span className="field-value">{studentName} ({studentId})</span>
        </div>

        <div className="form-field">
          <label>Date:</label>
          <span className="field-value">{date}</span>
        </div>

        <div className="form-field">
          <label>Status:</label>
          <div className="status-toggle-group">
            <button
              type="button"
              className={`toggle-btn ${status === 'ABSENT' ? 'active-absent' : ''}`}
              onClick={() => setStatus('ABSENT')}
              disabled={!!resultMsg && !isError}
            >
              ABSENT
            </button>
            <button
              type="button"
              className={`toggle-btn ${status === 'PRESENT' ? 'active-present' : ''}`}
              onClick={() => setStatus('PRESENT')}
              disabled={!!resultMsg && !isError}
            >
              PRESENT
            </button>
          </div>
        </div>

        {resultMsg ? (
          <div className={`form-feedback ${isError ? 'error' : 'success'}`}>
            {isError ? <AlertTriangle size={16} /> : <CheckCircle size={16} />}
            <span>{resultMsg}</span>
          </div>
        ) : (
          <div className="form-actions">
            <button className="confirm-btn" onClick={handleConfirm} disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 size={16} className="spin" /> Updating...
                </>
              ) : (
                'Confirm'
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
