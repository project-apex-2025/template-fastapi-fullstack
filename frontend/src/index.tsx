import React from 'react';
import ReactDOM from 'react-dom/client';
import { configureAuth } from './auth/amplifyConfig';
import App from './App';

configureAuth();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
