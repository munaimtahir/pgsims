import { afterEach, describe, expect, it, jest } from '@jest/globals';
import apiClient from './client';
import { supervisionApi as api } from './supervision';

afterEach(() => jest.restoreAllMocks());

describe('supervision API contracts', () => {
  it('unwraps assignment collections and preserves filters', async () => {
    const get = jest.spyOn(apiClient, 'get');
    get.mockResolvedValueOnce({ data: [{ id: 1 }] } as never);
    expect(await api.listAssignments()).toEqual([{ id: 1 }]);
    expect(get).toHaveBeenLastCalledWith('/api/supervision/assignments/', { params: undefined });
    get.mockResolvedValueOnce({ data: { count: 1, results: [{ id: 2 }] } } as never);
    expect(await api.listAssignments({ status: 'ACTIVE', resident: 7 })).toEqual([{ id: 2 }]);
    expect(get).toHaveBeenLastCalledWith('/api/supervision/assignments/', { params: { status: 'ACTIVE', resident: 7 } });
    get.mockResolvedValueOnce({ data: {} } as never);
    expect(await api.listAssignments()).toEqual([]);
  });

  it.each([
    ['assignments/7/', () => api.getAssignment(7), ['/api/supervision/assignments/7/']],
    ['options/', () => api.getSupervisionOptions({ department: 3 }), ['/api/supervision/options/', { params: { department: 3 } }]],
    ['data-quality/', () => api.getSupervisionDataQuality(), ['/api/supervision/data-quality/']],
  ])('reads %s', async (_path, read, expectedArgs) => {
    const get = jest.spyOn(apiClient, 'get').mockResolvedValue({ data: { id: 7 } } as never);
    expect(await read()).toEqual({ id: 7 });
    expect(get.mock.calls).toContainEqual(expectedArgs);
  });

  it('creates, ends and changes assignments using their dedicated contracts', async () => {
    const post = jest.spyOn(apiClient, 'post').mockResolvedValue({ data: { id: 7 } } as never);
    const create = { resident_id: 1, supervisor_id: 2, start_date: '2026-01-01' };
    expect(await api.createAssignment(create)).toEqual({ id: 7 });
    expect(await api.endAssignment(7, { end_date: '2026-02-01', reason_for_change: 'Rotation ended' })).toEqual({ id: 7 });
    expect(await api.changePrimary({ resident_id: 1, new_supervisor_id: 3, start_date: '2026-02-02' })).toEqual({ id: 7 });
    expect(post).toHaveBeenNthCalledWith(1, '/api/supervision/assignments/', create);
    expect(post).toHaveBeenNthCalledWith(2, '/api/supervision/assignments/7/end/', { end_date: '2026-02-01', reason_for_change: 'Rotation ended' });
    expect(post).toHaveBeenNthCalledWith(3, '/api/supervision/change-primary/', { resident_id: 1, new_supervisor_id: 3, start_date: '2026-02-02' });
  });

  it('uploads a CSV with dry-run selection and preserves failures', async () => {
    const post = jest.spyOn(apiClient, 'post').mockResolvedValue({ data: { success: true, dry_run: false, successes: [], failures: [] } } as never);
    const file = new File(['resident,supervisor'], 'assignments.csv', { type: 'text/csv' });
    expect(await api.importSupervisionCsv(file, false)).toEqual({ success: true, dry_run: false, successes: [], failures: [] });
    expect(post).toHaveBeenCalledWith('/api/supervision/import/', expect.any(FormData), { headers: { 'Content-Type': 'multipart/form-data' } });
    const [, form] = post.mock.calls[0];
    expect((form as FormData).get('file')).toBe(file);
    expect((form as FormData).get('dry_run')).toBe('false');
    const failure = new Error('network unavailable');
    post.mockRejectedValueOnce(failure);
    await expect(api.createAssignment({ resident_id: 1, supervisor_id: 2, start_date: '2026-01-01' })).rejects.toBe(failure);
  });
});
