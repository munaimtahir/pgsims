import { afterEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { bulkApi } from './bulk';
import apiClient from './client';

jest.mock('./client', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
}));

describe('bulkApi', () => {
  const mockedPost = apiClient.post as jest.MockedFunction<(...args: unknown[]) => Promise<{ data: unknown }>>;

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('importEntity calls correct endpoint', async () => {
    mockedPost.mockResolvedValue({ data: {} });
    const file = new File([''], 'test.csv');
    await bulkApi.importEntity('residents', file, 'apply');
    expect(apiClient.post).toHaveBeenCalledWith(
      '/api/bulk/import/residents/apply/',
      expect.any(FormData),
      expect.any(Object)
    );
  });
});
