/**
 * PARTH ASSISTANT AI — API Configuration
 * Reads base URL dynamically from environment variable or active hostname.
 */
const isLocalhost = typeof window !== 'undefined' && 
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 
  (isLocalhost ? 'http://localhost:8000' : '')
).replace(/\/+$/, '');
