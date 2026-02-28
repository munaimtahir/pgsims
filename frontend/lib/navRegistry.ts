/**
 * Canonical nav registry — single source of truth for all sidebar navigation.
 * Role-based sections drive what each user sees.
 */

export type AppRole =
  | 'admin'
  | 'utrmc_admin'
  | 'utrmc_user'
  | 'supervisor'
  | 'faculty'
  | 'pg'
  | 'resident';

export interface NavItem {
  label: string;
  href: string;
  icon: string; // Heroicons outline name (snake_case)
}

export interface NavSection {
  title: string;
  allowedRoles: AppRole[];
  items: (NavItem & { allowedRoles?: AppRole[] })[];
}

export const NAV_SECTIONS: NavSection[] = [
  // ------------------------------------------------------------------ Admin
  {
    title: 'Admin Console',
    allowedRoles: ['admin'],
    items: [
      { label: 'Overview', href: '/dashboard/admin', icon: 'home' },
      { label: 'Users', href: '/dashboard/admin/users', icon: 'users' },
      { label: 'Analytics', href: '/dashboard/admin/analytics', icon: 'chart-bar' },
      { label: 'Audit Logs', href: '/dashboard/admin/audit-logs', icon: 'clipboard-list' },
      { label: 'Reports', href: '/dashboard/admin/reports', icon: 'document-text' },
    ],
  },

  // ------------------------------------------------------------------ UTRMC
  {
    title: 'UTRMC',
    allowedRoles: ['admin', 'utrmc_admin', 'utrmc_user'],
    items: [
      { label: 'Overview', href: '/dashboard/utrmc', icon: 'view-grid' },
      { label: 'Hospitals', href: '/dashboard/utrmc/hospitals', icon: 'office-building', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'Departments', href: '/dashboard/utrmc/departments', icon: 'academic-cap', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'H-D Matrix', href: '/dashboard/utrmc/matrix', icon: 'table', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'Users', href: '/dashboard/utrmc/users', icon: 'user-group', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'Supervision Links', href: '/dashboard/utrmc/linking/supervision', icon: 'link', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'HOD Assignments', href: '/dashboard/utrmc/linking/hod', icon: 'star', allowedRoles: ['admin', 'utrmc_admin'] },
      { label: 'Cases', href: '/dashboard/utrmc/cases', icon: 'folder' },
      { label: 'Reports', href: '/dashboard/utrmc/reports', icon: 'document-report' },
    ],
  },

  // ------------------------------------------------------------------ Data Admin
  {
    title: 'Data Admin',
    allowedRoles: ['admin', 'utrmc_admin'],
    items: [
      { label: 'Import Hospitals', href: '/dashboard/utrmc/data-admin/hospitals', icon: 'upload' },
      { label: 'Import Departments', href: '/dashboard/utrmc/data-admin/departments', icon: 'upload' },
      { label: 'Import Matrix', href: '/dashboard/utrmc/data-admin/matrix', icon: 'upload' },
      { label: 'Import Supervisors', href: '/dashboard/utrmc/data-admin/supervisors', icon: 'upload' },
      { label: 'Import Residents', href: '/dashboard/utrmc/data-admin/residents', icon: 'upload' },
      { label: 'Import Links', href: '/dashboard/utrmc/data-admin/links', icon: 'link' },
      { label: 'Export Data', href: '/dashboard/utrmc/data-admin/export', icon: 'download' },
      { label: 'Templates', href: '/dashboard/utrmc/data-admin/templates', icon: 'template' },
    ],
  },

  // ------------------------------------------------------------------ Supervisor
  {
    title: 'Supervisor',
    allowedRoles: ['supervisor', 'faculty'],
    items: [
      { label: 'Overview', href: '/dashboard/supervisor', icon: 'home' },
      { label: 'Logbooks', href: '/dashboard/supervisor/logbooks', icon: 'book-open' },
      { label: 'Cases', href: '/dashboard/supervisor/cases', icon: 'folder-open' },
      { label: 'My PGs', href: '/dashboard/supervisor/pgs', icon: 'users' },
    ],
  },

  // ------------------------------------------------------------------ PG / Resident
  {
    title: 'My Training',
    allowedRoles: ['pg', 'resident'],
    items: [
      { label: 'Overview', href: '/dashboard/pg', icon: 'home' },
      { label: 'Logbook', href: '/dashboard/pg/logbook', icon: 'book-open' },
      { label: 'Cases', href: '/dashboard/pg/cases', icon: 'folder-open' },
      { label: 'Rotations', href: '/dashboard/pg/rotations', icon: 'refresh' },
      { label: 'Results', href: '/dashboard/pg/results', icon: 'chart-bar' },
      { label: 'Certificates', href: '/dashboard/pg/certificates', icon: 'badge-check' },
      { label: 'Notifications', href: '/dashboard/pg/notifications', icon: 'bell' },
    ],
  },
];

/**
 * Return nav sections visible to a given role.
 * Items within a section are also filtered by item-level allowedRoles if set.
 */
export function getNavForRole(role: AppRole | string): NavSection[] {
  return NAV_SECTIONS.filter((s) => s.allowedRoles.includes(role as AppRole))
    .map((s) => ({
      ...s,
      items: s.items.filter(
        (item) => !item.allowedRoles || item.allowedRoles.includes(role as AppRole)
      ),
    }))
    .filter((s) => s.items.length > 0);
}
