import RoleDirectoryPage from '@/components/directory/RoleDirectoryPage';

export default function UsersPage() {
  return (
    <RoleDirectoryPage
      title="Users"
      description="Canonical universal identity directory for all active PGMS roles."
      createHref="/users/new"
    />
  );
}
