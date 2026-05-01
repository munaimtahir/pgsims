import { getDashboardPathForRole, getRoleLabel, isUtrmcManagerRole, isUtrmcReadonlyRole } from './rbac';

describe('rbac utilities', () => {
  describe('getDashboardPathForRole', () => {
    it('returns /dashboard/utrmc for utrmc roles', () => {
      expect(getDashboardPathForRole('admin')).toBe('/dashboard/utrmc');
      expect(getDashboardPathForRole('utrmc_admin')).toBe('/dashboard/utrmc');
      expect(getDashboardPathForRole('utrmc_user')).toBe('/dashboard/utrmc');
    });

    it('returns /dashboard/supervisor for supervisor roles', () => {
      expect(getDashboardPathForRole('supervisor')).toBe('/dashboard/supervisor');
      expect(getDashboardPathForRole('faculty')).toBe('/dashboard/supervisor');
    });

    it('returns /dashboard/resident for pg roles', () => {
      expect(getDashboardPathForRole('pg')).toBe('/dashboard/resident');
      expect(getDashboardPathForRole('resident')).toBe('/dashboard/resident');
    });

    it('returns /unauthorized for unknown or null roles', () => {
      expect(getDashboardPathForRole(null)).toBe('/unauthorized');
      expect(getDashboardPathForRole(undefined)).toBe('/unauthorized');
      expect(getDashboardPathForRole('guest')).toBe('/unauthorized');
    });
  });

  describe('getRoleLabel', () => {
    it('returns custom labels for utrmc roles', () => {
      expect(getRoleLabel('utrmc_user')).toBe('UTRMC Read-only');
      expect(getRoleLabel('utrmc_admin')).toBe('UTRMC Admin');
    });

    it('returns input role or unknown for others', () => {
      expect(getRoleLabel('pg')).toBe('pg');
      expect(getRoleLabel(null)).toBe('unknown');
    });
  });

  describe('isUtrmcManagerRole', () => {
    it('returns true for admin and utrmc_admin', () => {
      expect(isUtrmcManagerRole('admin')).toBe(true);
      expect(isUtrmcManagerRole('utrmc_admin')).toBe(true);
    });

    it('returns false for others', () => {
      expect(isUtrmcManagerRole('utrmc_user')).toBe(false);
      expect(isUtrmcManagerRole('pg')).toBe(false);
    });
  });

  describe('isUtrmcReadonlyRole', () => {
    it('returns true for utrmc_user', () => {
      expect(isUtrmcReadonlyRole('utrmc_user')).toBe(true);
    });

    it('returns false for others', () => {
      expect(isUtrmcReadonlyRole('utrmc_admin')).toBe(false);
      expect(isUtrmcReadonlyRole('admin')).toBe(false);
    });
  });
});
