/**
 * Canonical nav registry — single source of truth for all sidebar navigation.
 * Role-based sections drive what each user sees.
 */

export type AppRole =
  | 'ADMIN'
  | 'RESIDENT'
  | 'SUPERVISOR'
  | 'SUPPORT_STAFF';

export interface NavSubItem {
  label: string;
  href: string;
  allowedRoles?: AppRole[];
}

export interface NavItem {
  label: string;
  href?: string;
  icon: string; // Heroicons outline name (snake_case)
  allowedRoles?: AppRole[];
  subItems?: NavSubItem[];
}

export interface NavSection {
  title: string;
  allowedRoles: AppRole[];
  items: NavItem[];
}

export const NAV_SECTIONS: NavSection[] = [
  // ------------------------------------------------------------------ Program Administration
  {
    title: 'Program Administration',
    allowedRoles: ['ADMIN', 'SUPPORT_STAFF'],
    items: [
      { label: 'Overview', href: '/dashboard/utrmc', icon: 'home' },
      { label: 'Hospitals', href: '/dashboard/utrmc/hospitals', icon: 'office-building' },
      { label: 'Departments', href: '/dashboard/utrmc/departments', icon: 'academic-cap' },
      { label: 'H-D Matrix', href: '/dashboard/utrmc/matrix', icon: 'table' },
      { label: 'Users', href: '/dashboard/utrmc/users', icon: 'users' },
      { label: 'Supervisors', href: '/dashboard/utrmc/supervisors', icon: 'user-group' },
      { label: 'Supervision Links', href: '/dashboard/utrmc/supervision', icon: 'link' },
      { label: 'Programmes', href: '/dashboard/utrmc/programs', icon: 'book-open' },
      { label: 'Eligibility Monitor', href: '/dashboard/utrmc/eligibility-monitoring', icon: 'chart-bar' },
      { label: 'Backup Center', href: '/dashboard/utrmc/backup', icon: 'download', allowedRoles: ['ADMIN'] },
    ],
  },

  // ------------------------------------------------------------------ Supervisor
  {
    title: 'Supervisory Dashboard',
    allowedRoles: ['SUPERVISOR'],
    items: [
      { label: 'Overview', href: '/dashboard/supervisor', icon: 'home' },
      { label: 'My Residents', href: '/dashboard/supervisor', icon: 'users' },
    ],
  },

  // ------------------------------------------------------------------ Resident / PG
  {
    title: 'Resident Portfolio',
    allowedRoles: ['RESIDENT'],
    items: [
      { label: 'My Dashboard', href: '/dashboard/resident', icon: 'home' },
      { label: 'My Schedule', href: '/dashboard/resident/schedule', icon: 'calendar' },
      { label: 'Logbook', href: '/dashboard/resident/progress', icon: 'chart-bar' },
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
      items: s.items
        .filter((item) => !item.allowedRoles || item.allowedRoles.includes(role as AppRole))
        .map((item) => {
          if (item.subItems) {
            return {
              ...item,
              subItems: item.subItems.filter(
                (sub) => !sub.allowedRoles || sub.allowedRoles.includes(role as AppRole)
              ),
            };
          }
          return item;
        })
        .filter((item) => !item.subItems || item.subItems.length > 0),
    }))
    .filter((s) => s.items.length > 0);
}
