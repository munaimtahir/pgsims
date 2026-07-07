import { getDashboardPathForRole, getRoleLabel, isUtrmcManagerRole, isUtrmcReadonlyRole } from './rbac';

describe('rbac utilities', () => {
  describe('getDashboardPathForRole', () => {
    it('returns /dashboard/utrmc for admin and support staff roles', () => {
      expect(getDashboardPathForRole('ADMIN')).toBe('/dashboard/utrmc');
      expect(getDashboardPathForRole('SUPPORT_STAFF')).toBe('/dashboard/utrmc');
    });

    it('returns /dashboard/supervisor for supervisor role', () => {
      expect(getDashboardPathForRole('SUPERVISOR')).toBe('/dashboard/supervisor');
    });

    it('returns /dashboard/resident for resident role', () => {
      expect(getDashboardPathForRole('RESIDENT')).toBe('/dashboard/resident');
    });

    it('returns /unauthorized for unknown or null roles', () => {
      expect(getDashboardPathForRole(null)).toBe('/unauthorized');
      expect(getDashboardPathForRole(undefined)).toBe('/unauthorized');
      expect(getDashboardPathForRole('guest')).toBe('/unauthorized');
    });
  });

  describe('getRoleLabel', () => {
    it('returns labels for canonical roles', () => {
      expect(getRoleLabel('SUPPORT_STAFF')).toBe('Support Staff');
      expect(getRoleLabel('ADMIN')).toBe('Admin');
    });

    it('returns input role or unknown for others', () => {
      expect(getRoleLabel('RESIDENT')).toBe('RESIDENT');
      expect(getRoleLabel(null)).toBe('unknown');
    });
  });

  describe('isUtrmcManagerRole', () => {
    it('returns true for admin', () => {
      expect(isUtrmcManagerRole('ADMIN')).toBe(true);
    });

    it('returns false for others', () => {
      expect(isUtrmcManagerRole('SUPPORT_STAFF')).toBe(false);
      expect(isUtrmcManagerRole('RESIDENT')).toBe(false);
    });
  });

  describe('isUtrmcReadonlyRole', () => {
    it('returns true for support staff', () => {
      expect(isUtrmcReadonlyRole('SUPPORT_STAFF')).toBe(true);
    });

    it('returns false for others', () => {
      expect(isUtrmcReadonlyRole('ADMIN')).toBe(false);
      expect(isUtrmcReadonlyRole('RESIDENT')).toBe(false);
    });
  });
});
