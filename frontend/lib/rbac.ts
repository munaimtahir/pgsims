export type AppRole =
  | 'ADMIN'
  | 'RESIDENT'
  | 'SUPERVISOR'
  | 'SUPPORT_STAFF';

export function getDashboardPathForRole(role?: string | null): string {
  switch (role) {
    case 'ADMIN':
      return '/dashboard/utrmc';
    case 'SUPPORT_STAFF':
      return '/dashboard';
    case 'SUPERVISOR':
      return '/dashboard/supervisor';
    case 'RESIDENT':
      return '/dashboard/resident';
    default:
      return '/unauthorized';
  }
}

export function getRoleLabel(role?: string | null): string {
  switch (role) {
    case 'SUPPORT_STAFF':
      return 'Support Staff';
    case 'ADMIN':
      return 'Admin';
    case 'RESIDENT':
      return 'Resident';
    case 'SUPERVISOR':
      return 'Supervisor';
    default:
      return role ?? 'unknown';
  }
}

export function isUtrmcManagerRole(role?: string | null): boolean {
  return role === 'ADMIN';
}

export function isUtrmcReadonlyRole(role?: string | null): boolean {
  return role === 'SUPPORT_STAFF';
}
