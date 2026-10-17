import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';
import axios from 'axios';

jest.mock('@/lib/auth/cookies', () => ({ clearAuthCookies: jest.fn(), syncAuthCookies: jest.fn() }));

import apiClient from './client';
import * as authCookies from '@/lib/auth/cookies';

type Interceptor = { fulfilled?: (value: any) => any; rejected?: (error: any) => any };
const requestInterceptor = () => (apiClient.interceptors.request as any).handlers[0] as Interceptor;
const responseInterceptor = () => (apiClient.interceptors.response as any).handlers[0] as Interceptor;

describe('apiClient authentication and refresh behavior', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  afterEach(() => {
    jest.restoreAllMocks();
    localStorage.clear();
  });

  it('adds an access token only when one is stored', async () => {
    const handler = requestInterceptor().fulfilled!;
    const anonymous = await handler({ headers: {} });
    expect(anonymous.headers.Authorization).toBeUndefined();
    localStorage.setItem('access_token', 'access-1');
    expect((await handler({ headers: {} })).headers.Authorization).toBe('Bearer access-1');
  });

  it('propagates request setup failures', async () => {
    const failure = new Error('bad request setup');
    await expect(requestInterceptor().rejected!(failure)).rejects.toBe(failure);
  });

  it('returns successful API responses unchanged', () => {
    const response = { data: { ok: true } };
    expect(responseInterceptor().fulfilled!(response)).toBe(response);
  });

  it('rotates access and refresh tokens then retries the original request once', async () => {
    localStorage.setItem('refresh_token', 'old-refresh');
    localStorage.setItem('user', JSON.stringify({ role: 'RESIDENT' }));
    const refresh = jest.spyOn(axios, 'post').mockResolvedValue({ data: { access: 'new-access', refresh: 'new-refresh' } } as never);
    const retry = jest.fn().mockResolvedValue({ data: { retried: true } });
    const result = await responseInterceptor().rejected!({ config: { headers: {}, url: '/api/items/', adapter: retry }, response: { status: 401 } });
    expect(refresh).toHaveBeenCalledWith('/api/auth/refresh/', { refresh: 'old-refresh' });
    expect(retry).toHaveBeenCalledWith(expect.objectContaining({ _retry: true, headers: expect.objectContaining({ Authorization: 'Bearer new-access' }) }));
    expect(localStorage.getItem('access_token')).toBe('new-access');
    expect(localStorage.getItem('refresh_token')).toBe('new-refresh');
    expect(authCookies.syncAuthCookies).toHaveBeenCalledWith({ accessToken: 'new-access', role: 'RESIDENT' });
    expect(result).toEqual(expect.objectContaining({ data: { retried: true } }));
  });

  it('keeps an existing refresh token when the backend does not rotate it', async () => {
    localStorage.setItem('refresh_token', 'old-refresh');
    jest.spyOn(axios, 'post').mockResolvedValue({ data: { access: 'new-access' } } as never);
    const retry = jest.fn().mockResolvedValue({ data: {} });
    await responseInterceptor().rejected!({ config: { headers: {}, adapter: retry }, response: { status: 401 } });
    expect(localStorage.getItem('refresh_token')).toBe('old-refresh');
    expect(authCookies.syncAuthCookies).toHaveBeenCalledWith({ accessToken: 'new-access', role: null });
  });

  it('clears the session and rejects when token refresh fails', async () => {
    localStorage.setItem('access_token', 'access');
    localStorage.setItem('refresh_token', 'refresh');
    localStorage.setItem('user', '{bad json');
    const refreshFailure = new Error('refresh rejected');
    jest.spyOn(axios, 'post').mockRejectedValue(refreshFailure);
    await expect(responseInterceptor().rejected!({ config: { headers: {} }, response: { status: 401 } })).rejects.toBe(refreshFailure);
    expect(localStorage.length).toBe(0);
    expect(authCookies.clearAuthCookies).toHaveBeenCalled();
  });

  it('does not refresh twice, refresh without a token, or non-401 failures', async () => {
    const log = jest.spyOn(console, 'error').mockImplementation(() => undefined);
    const refresh = jest.spyOn(axios, 'post');
    const cases = [
      { config: { _retry: true, url: '/already' }, response: { status: 401, data: {} } },
      { config: { url: '/missing-token' }, response: { status: 401, data: {} } },
      { config: { url: '/forbidden' }, response: { status: 403, data: {} } },
      { config: { url: '/network' }, request: {}, message: 'offline' },
      { config: { url: '/setup' }, message: 'bad config' },
    ];
    for (const error of cases) await expect(responseInterceptor().rejected!(error)).rejects.toBe(error);
    expect(refresh).not.toHaveBeenCalled();
    expect(log).toHaveBeenCalledTimes(cases.length);
  });
});
