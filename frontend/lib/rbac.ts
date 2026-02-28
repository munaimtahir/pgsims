export type AppRole =
  | 'pg'
  | 'resident'
  | 'supervisor'
  | 'faculty'
  | 'admin'
  | 'utrmc_user'
  | 'utrmc_admin';

export function getDashboardPathForRole(role?: string | null): string {
  switch (role) {
    case 'admin':
      return '/dashboard/admin';
    case 'supervisor':
    case 'faculty':
      return '/dashboard/supervisor';
    case 'pg':
    case 'resident':
      return '/dashboard/pg';
    case 'utrmc_user':
    case 'utrmc_admin':
      return '/dashboard/utrmc';
    default:
      return '/unauthorized';
  }
}

export function getRoleLabel(role?: string | null): string {
  switch (role) {
    case 'utrmc_user':
      return 'UTRMC Read-only';
    case 'utrmc_admin':
      return 'UTRMC Admin';
    default:
      return role ?? 'unknown';
  }
}
