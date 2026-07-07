import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { userbaseApi } from './userbase';
import apiClient from './client';

describe('userbaseApi', () => {
  let getSpy: jest.SpiedFunction<typeof apiClient.get>;

  beforeEach(() => {
    getSpy = jest.spyOn(apiClient, 'get');
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
    await userbaseApi.users.list({ role: 'RESIDENT' });
    expect(apiClient.get).toHaveBeenCalledWith('/api/users/', { params: { role: 'RESIDENT' } });
  });
});
