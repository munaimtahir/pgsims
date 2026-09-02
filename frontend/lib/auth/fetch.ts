export const fetchAuth = async (url: string, options: RequestInit = {}) => {
  if (typeof window === 'undefined') {
    return fetch(url, options);
  }

  const token = localStorage.getItem('access_token');
  const headers = new Headers(options.headers || {});
  
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  
  // If body is JSON and Content-Type is not set, set it
  if (options.body && typeof options.body === 'string' && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
};
