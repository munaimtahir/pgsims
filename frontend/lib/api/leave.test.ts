import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { leaveApi } from './leave';
import apiClient from './client';

describe('leaveApi', () => {
  let getSpy: jest.SpiedFunction<typeof apiClient.get>;
  let postSpy: jest.SpiedFunction<typeof apiClient.post>;

  beforeEach(() => {
    getSpy = jest.spyOn(apiClient, 'get');
    postSpy = jest.spyOn(apiClient, 'post');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('list calls /api/leaves/ and unwraps paginated results', async () => {
    getSpy.mockResolvedValue({ data: { count: 1, results: [{ id: 1 }] } } as never);
    const results = await leaveApi.list();
    expect(apiClient.get).toHaveBeenCalledWith('/api/leaves/', { params: undefined });
    expect(results).toEqual([{ id: 1 }]);
  });

  it('submit posts to the submit action endpoint', async () => {
    postSpy.mockResolvedValue({ data: { id: 5, status: 'SUBMITTED' } } as never);
    const result = await leaveApi.submit(5);
    expect(apiClient.post).toHaveBeenCalledWith('/api/leaves/5/submit/');
    expect(result.status).toBe('SUBMITTED');
  });

  it('reject posts the reason in the request body', async () => {
    postSpy.mockResolvedValue({ data: { id: 5, status: 'REJECTED' } } as never);
    await leaveApi.reject(5, 'Not enough notice');
    expect(apiClient.post).toHaveBeenCalledWith('/api/leaves/5/reject/', {
      reason: 'Not enough notice',
    });
  });
});
