import { getStatusLabel, getStatusBadgeClass } from './status';

describe('status utilities', () => {
  describe('getStatusLabel', () => {
    it('returns correct labels for known statuses', () => {
      expect(getStatusLabel('pending')).toBe('Submitted');
      expect(getStatusLabel('returned')).toBe('Returned');
      expect(getStatusLabel('rejected')).toBe('Rejected');
      expect(getStatusLabel('approved')).toBe('Approved');
      expect(getStatusLabel('draft')).toBe('Draft');
      expect(getStatusLabel('archived')).toBe('Archived');
    });

    it('returns input status or Unknown for others', () => {
      expect(getStatusLabel('active')).toBe('active');
      expect(getStatusLabel(null)).toBe('Unknown');
    });
  });

  describe('getStatusBadgeClass', () => {
    it('returns correct classes for statuses', () => {
      expect(getStatusBadgeClass('pending')).toContain('bg-yellow-100');
      expect(getStatusBadgeClass('returned')).toContain('bg-orange-100');
      expect(getStatusBadgeClass('approved')).toContain('bg-green-100');
      expect(getStatusBadgeClass('rejected')).toContain('bg-red-100');
      expect(getStatusBadgeClass('draft')).toContain('bg-gray-100');
    });

    it('returns default class for unknown status', () => {
      expect(getStatusBadgeClass('unknown')).toContain('bg-gray-100');
    });
  });
});
