import React, { useState } from 'react';
import { Database, ShieldCheck, Layers } from 'lucide-react';

export default function DatabaseView({ data = {} }) {
  const [selectedCollection, setSelectedCollection] = useState('Students');

  const collections = data.collections || [
    { name: 'Students', count: 120 },
    { name: 'Parents', count: 85 },
    { name: 'Teachers', count: 24 },
    { name: 'Attendance', count: 8420 },
    { name: 'Classes', count: 12 },
    { name: 'Subjects', count: 36 }
  ];

  return (
    <div className="context-card database-view-card animate-fade-in">
      <div className="card-header-badge">
        <Database size={18} className="text-accent" />
        <span>School Database</span>
        <span className="auth-secured-badge">
          <ShieldCheck size={12} /> Authorized Access
        </span>
      </div>

      <div className="db-body">
        <h4 className="section-title">
          <Layers size={14} /> Collections
        </h4>

        <div className="collections-grid">
          {collections.map((col) => (
            <div
              key={col.name}
              className={`collection-tile ${selectedCollection === col.name ? 'active' : ''}`}
              onClick={() => setSelectedCollection(col.name)}
            >
              <span className="col-name">{col.name}</span>
              <span className="col-count">{col.count.toLocaleString()}</span>
            </div>
          ))}
        </div>

        <div className="collection-quick-actions">
          {['Students', 'Attendance', 'Teachers'].map((colName) => (
            <button
              key={colName}
              className={`action-btn-pill ${selectedCollection === colName ? 'selected' : ''}`}
              onClick={() => setSelectedCollection(colName)}
            >
              [{colName}]
            </button>
          ))}
        </div>

        <div className="collection-preview">
          <div className="preview-header">
            <span>Viewing: {selectedCollection} Collection</span>
            <span className="secure-tag">Clean Schema (No Secrets)</span>
          </div>
          <div className="preview-meta-info">
            Collection index healthy • RBAC policy strictly enforced
          </div>
        </div>
      </div>
    </div>
  );
}
