import axios from "axios";

// Falls back to localhost for local dev; set VITE_API_URL in frontend/.env
// once the backend is deployed somewhere other than localhost.
export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: API_BASE_URL });

export default api;
