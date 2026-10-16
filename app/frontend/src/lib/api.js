const API_URL = (import.meta.env?.VITE_API_URL || '/api').replace(/\/$/, '');

export function apiFetch(path, options = {}) {
    const { authenticated = false, ...requestOptions } = options;
    const headers = new Headers(requestOptions.headers);
    if (authenticated) {
        const token = localStorage.getItem('access_token');
        if (token) headers.set('Authorization', `Bearer ${token}`);
    }
    return fetch(`${API_URL}${path}`, { ...requestOptions, headers });
}

export function apiErrorMessage(data, fallback) {
    if (typeof data.detail === 'string') return data.detail;
    if (Array.isArray(data.detail)) {
        return data.detail.map(error => error.msg).join('; ');
    }
    return fallback;
}
