import RoleDirectoryPage from '@/components/directory/RoleDirectoryPage';

export default function AdminsPage() {
  return (
    <RoleDirectoryPage
      title="Admins"
      description="Administrative users with canonical PGMS management access."
      role="ADMIN"
      detailBasePath="/admins"
      createHref="/users/new?role=ADMIN"
    />
  );
}
