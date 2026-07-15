import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';

const masterDomains = [
  {
    title: 'Hospitals',
    description: 'Training sites and hospitals used across resident, supervision, and academic setup.',
  },
  {
    title: 'Departments',
    description: 'Departments and department rosters used by canonical user and supervision flows.',
  },
  {
    title: 'Hospital-Department Matrix',
    description: 'Hospital/department master mapping used by assignments and master setup.',
  },
  {
    title: 'Programs',
    description: 'Training programmes and related academic master definitions.',
  },
];

export default function MastersPage() {
  return (
    <ProtectedRoute allowedRoles={['ADMIN']}>
      <div className="pg-page space-y-6">
        <PageHeader
          title="Masters"
          description="Canonical master-data hub for hospitals, departments, matrix setup, and programs. Duplicate UTRMC subpages have been retired."
        />
        <div className="grid gap-4 md:grid-cols-2">
          {masterDomains.map((item) => (
            <div key={item.title} className="rounded-2xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900">{item.title}</h2>
              <p className="mt-2 text-sm text-slate-600">{item.description}</p>
              <p className="mt-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                Managed through the canonical masters surface and backend registries
              </p>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
