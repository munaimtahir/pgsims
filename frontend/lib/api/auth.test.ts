import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { authApi } from './auth';
import apiClient from './client';

describe('authApi', () => {
  let postSpy: jest.SpiedFunction<typeof apiClient.post>;

  beforeEach(() => {
    postSpy = jest.spyOn(apiClient, 'post');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    localStorage.clear();
  });

  it('login calls correct endpoint', async () => {
    postSpy.mockResolvedValue({ data: { access: 'tok' } } as never);
    await authApi.login({ username: 'user', password: 'pass' });
    expect(apiClient.post).toHaveBeenCalledWith('/api/auth/login/', { username: 'user', password: 'pass' });
  });

  it('logout calls correct endpoint if refresh token exists', async () => {
    localStorage.setItem('refresh_token', 'ref-tok');
    postSpy.mockResolvedValue({ data: {} } as never);
    await authApi.logout();
    expect(apiClient.post).toHaveBeenCalledWith('/api/auth/logout/', { refresh: 'ref-tok' });
  });
});
