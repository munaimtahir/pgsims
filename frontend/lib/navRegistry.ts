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
  // ------------------------------------------------------------------ Admin Console
  {
    title: 'System Admin',
    allowedRoles: ['admin'],
    items: [
      { label: 'Overview', href: '/dashboard/admin', icon: 'home' },
      { label: 'Users & Roles', href: '/dashboard/admin/users', icon: 'users' },
      {
        label: 'System Monitoring',
        icon: 'chart-bar',
        subItems: [
          { label: 'Analytics', href: '/dashboard/admin/analytics' },
          { label: 'Audit Logs', href: '/dashboard/admin/audit-logs' },
          { label: 'System Reports', href: '/dashboard/admin/reports' },
        ],
      },
    ],
  },

  // ------------------------------------------------------------------ Program Administration (Formerly UTRMC)
  {
    title: 'Program Administration',
    allowedRoles: ['admin', 'utrmc_admin', 'utrmc_user'],
    items: [
      { label: 'Dashboard', href: '/dashboard/utrmc', icon: 'view-grid' },
      {
        label: 'Institution Setup',
        icon: 'office-building',
        allowedRoles: ['admin', 'utrmc_admin'],
        subItems: [
          { label: 'Hospitals', href: '/dashboard/utrmc/hospitals' },
          { label: 'Departments', href: '/dashboard/utrmc/departments' },
          { label: 'H-D Matrix', href: '/dashboard/utrmc/matrix' },
        ],
      },
      {
        label: 'User Management',
        icon: 'user-group',
        allowedRoles: ['admin', 'utrmc_admin'],
        subItems: [
          { label: 'All Users', href: '/dashboard/utrmc/users' },
          { label: 'Supervision Links', href: '/dashboard/utrmc/linking/supervision' },
          { label: 'HOD Assignments', href: '/dashboard/utrmc/linking/hod' },
        ],
      },
      {
        label: 'Academic Config',
        icon: 'academic-cap',
        allowedRoles: ['admin', 'utrmc_admin'],
        subItems: [
          { label: 'Programs', href: '/dashboard/utrmc/programs' },
          { label: 'Rotation Templates', href: '/dashboard/utrmc/program-templates' },
        ],
      },
      {
        label: 'Trainee Management',
        icon: 'users',
        allowedRoles: ['admin', 'utrmc_admin'],
        subItems: [
          { label: 'Resident Records', href: '/dashboard/utrmc/resident-training' },
          { label: 'Rotations', href: '/dashboard/utrmc/rotations' },
          { label: 'Postings', href: '/dashboard/utrmc/postings' },
          { label: 'Leaves', href: '/dashboard/utrmc/leaves' },
        ],
      },
      {
        label: 'Approvals',
        icon: 'check-circle',
        allowedRoles: ['admin', 'utrmc_admin'],
        subItems: [
          { label: 'Rotations', href: '/dashboard/utrmc/approvals/rotations' },
          { label: 'Leaves', href: '/dashboard/utrmc/approvals/leaves' },
        ],
      },
      {
        label: 'Records & Reports',
        icon: 'folder',
        subItems: [
          { label: 'Cases', href: '/dashboard/utrmc/cases' },
          { label: 'Reports', href: '/dashboard/utrmc/reports' },
        ],
      },
    ],
  },

  // ------------------------------------------------------------------ Data Operations
  {
    title: 'Data Operations',
    allowedRoles: ['admin', 'utrmc_admin'],
    items: [
      {
        label: 'Import Config',
        icon: 'upload',
        subItems: [
          { label: 'Hospitals', href: '/dashboard/utrmc/data-admin/hospitals' },
          { label: 'Departments', href: '/dashboard/utrmc/data-admin/departments' },
          { label: 'Matrix', href: '/dashboard/utrmc/data-admin/matrix' },
          { label: 'Programs', href: '/dashboard/utrmc/data-admin/training-programs' },
          { label: 'Templates', href: '/dashboard/utrmc/data-admin/rotation-templates' },
        ],
      },
      {
        label: 'Import Personnel',
        icon: 'user-group',
        subItems: [
          { label: 'Supervisors', href: '/dashboard/utrmc/data-admin/supervisors' },
          { label: 'Residents/PGs', href: '/dashboard/utrmc/data-admin/residents' },
          { label: 'Supervision Links', href: '/dashboard/utrmc/data-admin/links' },
          { label: 'Training Records', href: '/dashboard/utrmc/data-admin/resident-training-records' },
        ],
      },
      {
        label: 'Exports & Templates',
        icon: 'download',
        subItems: [
          { label: 'Export Data', href: '/dashboard/utrmc/data-admin/export' },
          { label: 'Templates', href: '/dashboard/utrmc/data-admin/templates' },
        ],
      },
    ],
  },

  // ------------------------------------------------------------------ Supervisor
  {
    title: 'Supervisory Dashboard',
    allowedRoles: ['supervisor', 'faculty'],
    items: [
      { label: 'Overview', href: '/dashboard/supervisor', icon: 'home' },
      { label: 'My Trainees (PGs)', href: '/dashboard/supervisor/pgs', icon: 'users' },
      {
        label: 'Academics',
        icon: 'book-open',
        subItems: [
          { label: 'Logbooks', href: '/dashboard/supervisor/logbooks' },
          { label: 'Cases', href: '/dashboard/supervisor/cases' },
        ],
      },
      {
        label: 'Rotations',
        icon: 'refresh',
        subItems: [
          { label: 'My Rotations', href: '/dashboard/supervisor/rotations' },
          { label: 'Approvals', href: '/dashboard/supervisor/approvals' },
        ],
      },
    ],
  },

  // ------------------------------------------------------------------ PG / Resident
  {
    title: 'Postgraduate Portfolio',
    allowedRoles: ['pg', 'resident'],
    items: [
      { label: 'Overview', href: '/dashboard/pg', icon: 'home' },
      {
        label: 'Academics',
        icon: 'book-open',
        subItems: [
          { label: 'Logbook', href: '/dashboard/pg/logbook' },
          { label: 'Cases', href: '/dashboard/pg/cases' },
        ],
      },
      {
        label: 'Training Schedule',
        icon: 'calendar',
        subItems: [
          { label: 'My Schedule', href: '/dashboard/my-training' },
          { label: 'Rotations', href: '/dashboard/pg/rotations' },
          { label: 'Leaves', href: '/dashboard/my-leaves' },
          { label: 'Postings', href: '/dashboard/my-postings' },
        ],
      },
      {
        label: 'Achievements',
        icon: 'badge-check',
        subItems: [
          { label: 'Results', href: '/dashboard/pg/results' },
          { label: 'Certificates', href: '/dashboard/pg/certificates' },
        ],
      },
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

