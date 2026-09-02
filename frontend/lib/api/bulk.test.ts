import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { bulkApi } from './bulk';
import apiClient from './client';

describe('bulkApi', () => {
  let postSpy: jest.SpiedFunction<typeof apiClient.post>;

  beforeEach(() => {
    postSpy = jest.spyOn(apiClient, 'post');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('importEntity calls correct endpoint', async () => {
    postSpy.mockResolvedValue({ data: {} } as never);
    const file = new File([''], 'test.csv');
    await bulkApi.importEntity('residents', file, 'apply');
    expect(apiClient.post).toHaveBeenCalledWith(
      '/api/bulk/import/residents/apply/',
      expect.any(FormData),
      expect.any(Object)
    );
  });
});
