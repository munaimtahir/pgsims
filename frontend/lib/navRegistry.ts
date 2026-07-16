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
  icon: string;
  allowedRoles?: AppRole[];
  subItems?: NavSubItem[];
}

export interface NavSection {
  title: string;
  allowedRoles: AppRole[];
  items: NavItem[];
}

export const NAV_SECTIONS: NavSection[] = [
  {
    title: 'Admin',
    allowedRoles: ['ADMIN'],
    items: [
      { label: 'Dashboard', href: '/dashboard/utrmc', icon: 'home' },
      { label: 'Users', href: '/users', icon: 'users' },
      { label: 'Residents', href: '/residents', icon: 'academic-cap' },
      { label: 'Supervisors', href: '/supervisors', icon: 'user-group' },
      { label: 'Support Staff', href: '/support-staff', icon: 'briefcase' },
      { label: 'Admins', href: '/admins', icon: 'shield-check' },
      { label: 'Masters', href: '/masters', icon: 'collection' },
      { label: 'Data Quality', href: '/dashboard/utrmc/data-quality', icon: 'chart-bar' },
      {
        label: 'Supervision',
        icon: 'link',
        subItems: [
          { label: 'Overview', href: '/supervision' },
          { label: 'Assignments', href: '/supervision/assignments' },
          { label: 'New Assignment', href: '/supervision/assignments/new' },
          { label: 'Import', href: '/supervision/import' },
          { label: 'Data Quality', href: '/supervision/data-quality' },
        ],
      },
      {
        label: 'Academics',
        icon: 'book-open',
        subItems: [
          { label: 'Overview', href: '/academics' },
          { label: 'Training Records', href: '/academics/training-records' },
          { label: 'Periods', href: '/academics/periods' },
          { label: 'Rotation Templates', href: '/academics/rotation-templates' },
          { label: 'Evaluation Templates', href: '/academics/evaluation-templates' },
          { label: 'Logbook Categories', href: '/academics/logbook-categories' },
          { label: 'Review Queue', href: '/academics/review-queue' },
          { label: 'Data Quality', href: '/academics/data-quality' },
        ],
      },
    ],
  },
  {
    title: 'Supervisor',
    allowedRoles: ['SUPERVISOR'],
    items: [
      { label: 'My Dashboard', href: '/dashboard/supervisor', icon: 'home' },
      { label: 'My Residents', href: '/dashboard/supervisor', icon: 'users' },
      { label: 'Supervision Ledger', href: '/dashboard/supervisor', icon: 'link' },
      { label: 'Academic Review Queue', href: '/academics/review-queue', icon: 'queue-list' },
      { label: 'My Profile', href: '/complete-profile', icon: 'user-circle' },
    ],
  },
  {
    title: 'Resident',
    allowedRoles: ['RESIDENT'],
    items: [
      { label: 'My Dashboard', href: '/dashboard/resident', icon: 'home' },
      { label: 'My Training', href: '/dashboard/resident', icon: 'academic-cap' },
      { label: 'My Supervisor', href: '/dashboard/resident', icon: 'user-group' },
      { label: 'My Academic Summary', href: '/dashboard/resident', icon: 'chart-bar' },
      { label: 'My Profile', href: '/complete-profile', icon: 'user-circle' },
    ],
  },
  {
    title: 'Support Staff',
    allowedRoles: ['SUPPORT_STAFF'],
    items: [
      { label: 'My Dashboard', href: '/dashboard', icon: 'home' },
      { label: 'My Profile', href: '/complete-profile', icon: 'user-circle' },
    ],
  },
];

export function getNavForRole(role: AppRole | string): NavSection[] {
  return NAV_SECTIONS.filter((section) => section.allowedRoles.includes(role as AppRole))
    .map((section) => ({
      ...section,
      items: section.items
        .filter((item) => !item.allowedRoles || item.allowedRoles.includes(role as AppRole))
        .map((item) => {
          if (!item.subItems) {
            return item;
          }
          return {
            ...item,
            subItems: item.subItems.filter(
              (subItem) => !subItem.allowedRoles || subItem.allowedRoles.includes(role as AppRole)
            ),
          };
        })
        .filter((item) => !item.subItems || item.subItems.length > 0),
    }))
    .filter((section) => section.items.length > 0);
}
