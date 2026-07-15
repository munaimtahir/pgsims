import RoleDirectoryPage from '@/components/directory/RoleDirectoryPage';

export default function ResidentsPage() {
  return (
    <RoleDirectoryPage
      title="Residents"
      description="Resident directory backed by the universal identity layer."
      role="RESIDENT"
      detailBasePath="/residents"
      createHref="/users/new?role=RESIDENT"
    />
  );
}
