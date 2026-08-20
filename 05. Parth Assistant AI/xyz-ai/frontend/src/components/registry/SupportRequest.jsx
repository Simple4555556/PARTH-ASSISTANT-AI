import React, { useState } from 'react';
import { PhoneCall, CheckCircle2, Loader2 } from 'lucide-react';

export default function SupportRequest({ data = {}, token, currentUser }) {
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [reqId, setReqId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const res = await fetch('http://localhost:8000/api/mock/support/call-request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          parent_id: currentUser?.user_id || 'P201',
          student_id: data.student_id || 'S101',
          teacher_id: data.teacher_id || 'T301',
          reason: reason || 'Discussion regarding child attendance and performance'
        })
      });

      if (!res.ok) throw new Error('Failed to submit call request');
      const resData = await res.json();
      setReqId(resData.request_id);
      setSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="context-card support-request-card animate-fade-in">
      <div className="card-header-badge">
        <PhoneCall size={18} className="text-accent" />
        <span>Request Teacher Call Back</span>
      </div>

      {submitted ? (
        <div className="form-feedback success" style={{ padding: '1rem', display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <CheckCircle2 size={24} className="text-success" />
          <div>
            <div style={{ fontWeight: 700 }}>Request Submitted!</div>
            <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>
              Reference ID: {reqId}. The teacher will reach out to you shortly.
            </div>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="support-form">
          <div className="form-field">
            <label>Reason for Callback:</label>
            <textarea
              className="chat-input"
              rows={3}
              placeholder="E.g., Discuss academic performance and attendance..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              style={{ width: '100%', resize: 'none', borderRadius: 8, padding: '0.5rem' }}
            />
          </div>

          <button type="submit" className="confirm-btn" disabled={isSubmitting}>
            {isSubmitting ? <Loader2 size={16} className="spin" /> : 'Submit Call Request'}
          </button>
        </form>
      )}
    </div>
  );
}
