'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { userbaseApi, DepartmentRosterResponse } from '@/lib/api/userbase';
import PageHeader from '@/components/ui/PageHeader';

export default function UTRMCDepartmentRosterPage() {
  const params = useParams();
  const departmentId = Number(params.id);
  const [roster, setRoster] = useState<DepartmentRosterResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    userbaseApi.departments
      .roster(departmentId)
      .then(setRoster)
      .catch(() => setError('Failed to load roster'))
      .finally(() => setLoading(false));
  }, [departmentId]);

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (error) return <p className="text-red-600">{error}</p>;
  if (!roster) return null;

  return (
    <div className="pg-page">
      <PageHeader
        title="Department Roster"
        description={`Department: ${roster.department.name}`}
      />
      {roster.hod && (
        <div className="pg-card">
          <h2 className="text-lg font-semibold text-gray-800">Head of Department</h2>
          <p className="text-gray-600">{roster.hod.full_name ?? roster.hod.username}</p>
        </div>
      )}
      {roster.supervisors.length > 0 && (
        <div className="pg-card">
          <h2 className="text-lg font-semibold text-gray-800">Supervisors</h2>
          <ul className="list-disc pl-5">
            {roster.supervisors.map((s) => (
              <li key={s.id} className="text-gray-600">
                {s.full_name ?? s.username}
              </li>
            ))}
          </ul>
        </div>
      )}
      {roster.residents.length > 0 && (
        <div className="pg-card">
          <h2 className="text-lg font-semibold text-gray-800">Residents</h2>
          <ul className="list-disc pl-5">
            {roster.residents.map((r) => (
              <li key={r.id} className="text-gray-600">
                {r.full_name ?? r.username}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
