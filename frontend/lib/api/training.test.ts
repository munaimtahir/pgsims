import apiClient from './client';
import { trainingApi } from './training';

jest.mock('./client', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
    post: jest.fn(),
    patch: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

const mockedGet = apiClient.get as jest.Mock;

describe('trainingApi eligibility contract', () => {
  beforeEach(() => {
    mockedGet.mockReset();
  });

  it('normalizes /api/my/eligibility/ envelope with reasons_json to reasons', async () => {
    mockedGet.mockResolvedValueOnce({
      data: {
        resident_training_record: 7,
        eligibilities: [
          {
            id: 1,
            milestone: 10,
            milestone_code: 'IMM',
            milestone_name: 'Intermediate Membership',
            status: 'NOT_READY',
            status_display: 'Not Ready',
            reasons_json: ['Workshop requirement not met'],
            computed_at: '2026-03-14T00:00:00Z',
          },
        ],
      },
    });

    const data = await trainingApi.getMyEligibility();

    expect(mockedGet).toHaveBeenCalledWith('/api/my/eligibility/');
    expect(data).toHaveLength(1);
    expect(data[0].reasons).toEqual(['Workshop requirement not met']);
  });

  it('normalizes /api/utrmc/eligibility/ results with reasons_json to reasons', async () => {
    mockedGet.mockResolvedValueOnce({
      data: {
        count: 1,
        results: [
          {
            id: 2,
            milestone: 11,
            milestone_code: 'FINAL',
            milestone_name: 'Final',
            status: 'PARTIALLY_READY',
            status_display: 'Partially Ready',
            reasons_json: ['Thesis not submitted'],
            computed_at: '2026-03-14T00:00:00Z',
          },
        ],
      },
    });

    const data = await trainingApi.getUTRMCEligibility();

    expect(mockedGet).toHaveBeenCalledWith('/api/utrmc/eligibility/', { params: undefined });
    expect(data.count).toBe(1);
    expect(data.results[0].reasons).toEqual(['Thesis not submitted']);
  });
});
