'use client';
import { useEffect, useState } from 'react';
import { userbaseApi } from '@/lib/api/userbase';

export default function UTRMCOverviewPage() {
  const [stats, setStats] = useState({ hospitals: 0, departments: 0, users: 0, supervisors: 0, residents: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      userbaseApi.hospitals.list(),
      userbaseApi.departments.list(),
      userbaseApi.users.list(),
    ]).then(([hospitals, departments, users]) => {
      setStats({
        hospitals: hospitals.length,
        departments: departments.length,
        users: users.length,
        supervisors: users.filter((u: any) => u.role === 'supervisor').length,
        residents: users.filter((u: any) => u.role === 'resident' || u.role === 'pg').length,
      });
    }).catch(() => setError('Failed to load stats')).finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  const cards = [
    { label: 'Hospitals', value: stats.hospitals },
    { label: 'Departments', value: stats.departments },
    { label: 'Total Users', value: stats.users },
    { label: 'Supervisors', value: stats.supervisors },
    { label: 'Residents / PGs', value: stats.residents },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">UTRMC Overview</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {cards.map((c) => (
          <div key={c.label} className="bg-white border border-gray-200 rounded-lg p-4">
            <p className="text-3xl font-bold text-indigo-600">{c.value}</p>
            <p className="text-sm text-gray-600 mt-1">{c.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
