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
    case 'utrmc_admin':
    case 'utrmc_user':
      return '/dashboard/utrmc';
    case 'supervisor':
    case 'faculty':
      return '/dashboard/supervisor';
    case 'pg':
    case 'resident':
      return '/dashboard/resident';
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
