import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { rotationsApi } from './rotations';
import apiClient from './client';

describe('rotationsApi', () => {
  let getSpy: jest.SpiedFunction<typeof apiClient.get>;

  beforeEach(() => {
    getSpy = jest.spyOn(apiClient, 'get');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('listHospitalDepartments follows pagination to collect every result', async () => {
    getSpy
      .mockResolvedValueOnce({
        data: { count: 51, next: '/api/hospital-departments/?page=2', results: Array(25).fill({ id: 1 }) },
      } as never)
      .mockResolvedValueOnce({
        data: { count: 51, next: '/api/hospital-departments/?page=3', results: Array(25).fill({ id: 2 }) },
      } as never)
      .mockResolvedValueOnce({
        data: { count: 51, next: null, results: Array(1).fill({ id: 3 }) },
      } as never);

    const results = await rotationsApi.listHospitalDepartments();

    expect(results).toHaveLength(51);
    expect(apiClient.get).toHaveBeenCalledTimes(3);
    expect(apiClient.get).toHaveBeenNthCalledWith(1, '/api/hospital-departments/', { params: { page: 1 } });
    expect(apiClient.get).toHaveBeenNthCalledWith(2, '/api/hospital-departments/', { params: { page: 2 } });
    expect(apiClient.get).toHaveBeenNthCalledWith(3, '/api/hospital-departments/', { params: { page: 3 } });
  });

  it('listResidentTrainingRecords stops after a single page when there is no next link', async () => {
    getSpy.mockResolvedValueOnce({
      data: { count: 2, next: null, results: [{ id: 1 }, { id: 2 }] },
    } as never);

    const results = await rotationsApi.listResidentTrainingRecords();

    expect(results).toHaveLength(2);
    expect(apiClient.get).toHaveBeenCalledTimes(1);
  });
});
