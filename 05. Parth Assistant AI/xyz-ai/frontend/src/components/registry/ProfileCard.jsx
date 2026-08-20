import React from 'react';
import { User } from 'lucide-react';

export default function ProfileCard({ data = {}, currentUser }) {
  const user = currentUser || {};
  return (
    <div className="context-card profile-card animate-fade-in">
      <div className="card-header-badge">
        <User size={18} className="text-accent" />
        <span>User Profile</span>
      </div>

      <div className="profile-details">
        <div className="profile-row">
          <span className="p-label">Name:</span>
          <span className="p-value">{user.name || 'User'}</span>
        </div>
        <div className="profile-row">
          <span className="p-label">Role:</span>
          <span className="p-value">{user.role}</span>
        </div>
        <div className="profile-row">
          <span className="p-label">User ID:</span>
          <span className="p-value">{user.user_id}</span>
        </div>
      </div>
    </div>
  );
}
