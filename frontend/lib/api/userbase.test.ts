import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { userbaseApi } from './userbase';
import apiClient from './client';

describe('userbaseApi', () => {
  let getSpy: jest.SpiedFunction<typeof apiClient.get>;
  let postSpy: jest.SpiedFunction<typeof apiClient.post>;

  beforeEach(() => {
    getSpy = jest.spyOn(apiClient, 'get');
    postSpy = jest.spyOn(apiClient, 'post');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('hospitals.list calls correct endpoint', async () => {
    getSpy.mockResolvedValue({ data: [] } as never);
    await userbaseApi.hospitals.list();
    expect(apiClient.get).toHaveBeenCalledWith('/api/hospitals/');
  });

  it('users.list calls correct endpoint with params', async () => {
    getSpy.mockResolvedValue({ data: [] } as never);
    await userbaseApi.users.list({
      role: 'resident',
      department: 7,
      supervisor: 3,
      program: 11,
      active: false,
      search: 'uro',
      is_complete_profile: true,
    });
    expect(apiClient.get).toHaveBeenCalledWith('/api/users/', {
      params: { role: 'resident', department: 7, supervisor: 3, program: 11, active: false, search: 'uro', is_complete_profile: true },
    });
  });

  it('users.resetPassword posts to the reset-password action', async () => {
    postSpy.mockResolvedValue({ data: { detail: 'ok' } } as never);
    await userbaseApi.users.resetPassword(42, 'pgfmu123');
    expect(apiClient.post).toHaveBeenCalledWith('/api/users/42/reset-password/', { password: 'pgfmu123' });
  });
});
