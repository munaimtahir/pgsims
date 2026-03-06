'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { userbaseApi, DepartmentRosterResponse } from '@/lib/api/userbase';

export default function PGDepartmentRosterPage() {
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
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Department Roster</h1>
      <p className="text-lg text-gray-700 mb-2">{roster.department.name}</p>
      {roster.hod && (
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-800">Head of Department</h2>
          <p className="text-gray-600">{roster.hod.full_name ?? roster.hod.username}</p>
        </div>
      )}
      {roster.supervisors.length > 0 && (
        <div className="mb-4">
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
        <div className="mb-4">
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
