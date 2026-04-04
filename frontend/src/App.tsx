import { useEffect, useState } from 'react';
import { useAuth } from './auth/useAuth';
import './index.css';

export default function App() {
  const { isAuthenticated, isLoading, alias, login, logout } = useAuth();
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  useEffect(() => {
    if (!isLoading && !isAuthenticated && window.location.pathname !== '/callback') login();
  }, [isLoading, isAuthenticated, login]);

  if (isLoading || !isAuthenticated) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontFamily: 'Inter, sans-serif' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', fontWeight: 700 }}>__APP_NAME__</div>
          <div style={{ color: '#A3A3A3', fontSize: '13px', marginTop: '8px' }}>Redirecting to login...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-name">__APP_NAME__</div>
        </div>
        <nav className="sidebar-nav">
          <button className="nav-item active">Home</button>
        </nav>
        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-user-avatar">{alias?.slice(0, 2).toUpperCase()}</div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">{alias}</div>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '4px' }}>
            <button className="theme-toggle" onClick={() => setDarkMode(d => !d)}>{darkMode ? '\u2600' : '\u263D'}</button>
            <button className="theme-toggle" onClick={logout} title="Sign out">\u23FB</button>
          </div>
        </div>
      </aside>
      <div className="app-main">
        <main className="app-content">
          <div className="view-header">
            <h1 className="view-title">Welcome</h1>
          </div>
          <div className="card" style={{ padding: '24px' }}>
            <p>Hello, <strong>{alias}</strong>! This app was provisioned by BioForge.</p>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Edit <code>src/App.tsx</code> to start building.</p>
          </div>
        </main>
      </div>
    </div>
  );
}
