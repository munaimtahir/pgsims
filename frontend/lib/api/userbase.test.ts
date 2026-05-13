/// <reference types="jest" />
import { userbaseApi } from './userbase';
import apiClient from './client';

jest.mock('./client', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
}));

describe('userbaseApi', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('hospitals.list calls correct endpoint', async () => {
    (apiClient.get as jest.Mock).mockResolvedValue({ data: [] });
    await userbaseApi.hospitals.list();
    expect(apiClient.get).toHaveBeenCalledWith('/api/hospitals/');
  });

  it('users.list calls correct endpoint with params', async () => {
    (apiClient.get as jest.Mock).mockResolvedValue({ data: [] });
    await userbaseApi.users.list({ role: 'resident' });
    expect(apiClient.get).toHaveBeenCalledWith('/api/users/', { params: { role: 'resident' } });
  });
});
