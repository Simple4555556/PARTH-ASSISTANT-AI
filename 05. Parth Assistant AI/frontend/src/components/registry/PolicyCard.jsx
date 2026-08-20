import React from 'react';
import { BookOpen, Award, ExternalLink, ShieldCheck } from 'lucide-react';

export default function PolicyCard({ data = {} }) {
  const title = data.title || "School Policy & Academic Guidelines";
  const category = data.category || "Official School Regulation";
  const citations = data.citations || [];

  return (
    <div className="context-card policy-card animate-fade-in">
      <div className="card-header-badge">
        <BookOpen size={18} className="text-accent" />
        <span>{title}</span>
        <span className="auth-secured-badge">
          <ShieldCheck size={12} /> Grounded Knowledge
        </span>
      </div>

      <div className="policy-card-body" style={{ marginTop: '0.75rem' }}>
        <div className="policy-meta-pill" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.35rem',
          fontSize: '0.75rem',
          background: 'rgba(59, 130, 246, 0.15)',
          color: '#60a5fa',
          padding: '0.25rem 0.6rem',
          borderRadius: '999px',
          marginBottom: '0.75rem',
          border: '1px solid rgba(59, 130, 246, 0.3)'
        }}>
          <Award size={12} />
          <span>Category: {category}</span>
        </div>

        {citations.length > 0 && (
          <div className="citations-container" style={{
            marginTop: '0.75rem',
            background: 'rgba(0, 0, 0, 0.25)',
            borderRadius: '10px',
            padding: '0.75rem',
            border: '1px solid var(--border-color)'
          }}>
            <div style={{
              fontSize: '0.75rem',
              fontWeight: 600,
              color: 'var(--text-muted)',
              marginBottom: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem'
            }}>
              <ExternalLink size={12} />
              <span>Verified School Citations & Sources:</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {citations.map((c, idx) => (
                <div key={idx} style={{
                  fontSize: '0.8rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  background: 'rgba(255, 255, 255, 0.03)',
                  padding: '0.4rem 0.6rem',
                  borderRadius: '6px'
                }}>
                  <span style={{ fontWeight: 600, color: '#93c5fd' }}>
                    {c.title} • {c.section}
                  </span>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                    {c.source}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
