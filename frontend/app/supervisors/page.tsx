import RoleDirectoryPage from '@/components/directory/RoleDirectoryPage';

export default function SupervisorsPage() {
  return (
    <RoleDirectoryPage
      title="Supervisors"
      description="Supervisor directory backed by the canonical supervision and identity modules."
      role="SUPERVISOR"
      detailBasePath="/supervisors"
      createHref="/users/new?role=SUPERVISOR"
    />
  );
}
