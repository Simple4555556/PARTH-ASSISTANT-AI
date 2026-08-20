import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ParthAssistantUI from './components/ParthAssistantUI';
import LoginScreen from './components/LoginScreen';

const DEMO_USERS = {
  STUDENT: {
    username: 'student1',
    name: 'Aarav Sharma',
    user_id: 'S101',
    role: 'STUDENT'
  },
  PARENT: {
    username: 'parent1',
    name: 'Rajesh Sharma',
    user_id: 'P201',
    role: 'PARENT'
  },
  TEACHER: {
    username: 'teacher1',
    name: 'Sunita Verma',
    user_id: 'T301',
    role: 'TEACHER'
  },
  PRINCIPAL: {
    username: 'principal1',
    name: 'Dr. V. K. Raman',
    user_id: 'M401',
    role: 'PRINCIPAL'
  }
};

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [activeRole, setActiveRole] = useState('STUDENT');
  const [currentUser, setCurrentUser] = useState(DEMO_USERS.STUDENT);
  const [token, setToken] = useState('');
  const [selectedLanguage, setLanguage] = useState('en');

  // Authenticate with backend whenever role changes
  useEffect(() => {
    if (!isAuthenticated) return;
    const user = DEMO_USERS[activeRole] || currentUser;

    fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user.username, password: 'password123' })
    })
      .then(res => res.json())
      .then(data => {
        if (data.access_token) {
          setToken(data.access_token);
        }
      })
      .catch(() => {});
  }, [activeRole, isAuthenticated]);

  const handleLoginSuccess = (loginData) => {
    setToken(loginData.token);
    setActiveRole(loginData.role);
    setCurrentUser(loginData.currentUser);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    if (token) {
      fetch('http://localhost:8000/api/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }).catch(() => {});
    }
    setIsAuthenticated(false);
    setToken('');
    setCurrentUser(DEMO_USERS.STUDENT);
  };

  if (!isAuthenticated) {
    return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }


  return (
    <div className="app-container">
      <Navbar
        activeRole={activeRole}
        setRole={(role) => {
          setActiveRole(role);
          setCurrentUser(DEMO_USERS[role]);
        }}
        currentUser={currentUser}
        selectedLanguage={selectedLanguage}
        setLanguage={setLanguage}
        onLogout={handleLogout}
      />

      <main>
        <ParthAssistantUI
          activeRole={activeRole}
          currentUser={currentUser}
          token={token}
          selectedLanguage={selectedLanguage}
          setLanguage={setLanguage}
        />
      </main>
    </div>
  );
}


