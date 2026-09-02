import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import BulkSetupWorkspace from '@/components/utrmc/BulkSetupWorkspace';

export default function MastersPage() {
  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Masters"
          description="Canonical master-data hub for hospitals, departments, matrix setup, programs, residents, supervisors, supervision links, and rotation placements. Duplicate UTRMC subpages have been retired."
        />
        <BulkSetupWorkspace />
      </div>
    </ProtectedRoute>
  );
}
