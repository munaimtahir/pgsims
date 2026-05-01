import { authApi } from './auth';
import apiClient from './client';

jest.mock('./client', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
}));

describe('authApi', () => {
  afterEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  it('login calls correct endpoint', async () => {
    (apiClient.post as jest.Mock).mockResolvedValue({ data: { access: 'tok' } });
    await authApi.login({ username: 'user', password: 'pass' });
    expect(apiClient.post).toHaveBeenCalledWith('/api/auth/login/', { username: 'user', password: 'pass' });
  });

  it('logout calls correct endpoint if refresh token exists', async () => {
    localStorage.setItem('refresh_token', 'ref-tok');
    (apiClient.post as jest.Mock).mockResolvedValue({ data: {} });
    await authApi.logout();
    expect(apiClient.post).toHaveBeenCalledWith('/api/auth/logout/', { refresh: 'ref-tok' });
  });
});
