import RoleDirectoryPage from '@/components/directory/RoleDirectoryPage';

export default function SupportStaffPage() {
  return (
    <RoleDirectoryPage
      title="Support Staff"
      description="Support staff directory for the active four-role system."
      role="SUPPORT_STAFF"
      detailBasePath="/support-staff"
      createHref="/users/new?role=SUPPORT_STAFF"
    />
  );
}
