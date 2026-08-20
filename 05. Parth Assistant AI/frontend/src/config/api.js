/**
 * PARTH ASSISTANT AI — API Configuration
 * Reads base URL dynamically from environment variable for Vercel & Production deployment.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '');
