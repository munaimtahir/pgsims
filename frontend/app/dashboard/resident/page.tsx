'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/authStore';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

import apiClient from '@/lib/api/client';

interface Rotation {
  id: number;
  department?: { name?: string } | string;
  hospital?: { name?: string } | string;
  start_date?: string;
  end_date?: string;
  status?: string;
}

export default function ResidentDashboardPage() {
  const { user } = useAuthStore();
  const [rotations, setRotations] = useState<Rotation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiClient.get('/api/my/rotations/')
      .then(r => {
        const data = r.data;
        setRotations(Array.isArray(data) ? data : data.results || []);
      })
      .catch(() => setError('Failed to load rotations'))
      .finally(() => setLoading(false));
  }, []);

  function getName(v: any): string {
    if (!v) return '—';
    if (typeof v === 'object') return v.name || '—';
    return String(v);
  }

  const current = rotations.find(r => r.status === 'active' || r.status === 'approved');

  return (
    <ProtectedRoute allowedRoles={['resident', 'pg']}>
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Resident Dashboard</h1>
          <p className="text-gray-600 mb-6">Welcome, {user?.full_name || user?.username || 'Resident'}</p>

          {current && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 mb-6">
              <h2 className="text-sm font-semibold text-indigo-800 mb-1">Current Rotation</h2>
              <p className="text-indigo-900 font-medium">{getName(current.department)} — {getName(current.hospital)}</p>
              <p className="text-indigo-600 text-xs mt-1">{current.start_date} → {current.end_date}</p>
            </div>
          )}

          <h2 className="text-lg font-semibold text-gray-800 mb-3">My Rotations</h2>
          {loading && <p className="text-gray-500">Loading...</p>}
          {error && <p className="text-red-600">{error}</p>}
          {!loading && !error && (
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>{['Department','Hospital','Start','End','Status'].map(h=><th key={h} className="text-left px-4 py-2 font-medium text-gray-600">{h}</th>)}</tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {rotations.length === 0 && <tr><td colSpan={5} className="px-4 py-4 text-center text-gray-400">No rotations found</td></tr>}
                  {rotations.map(r=>(
                    <tr key={r.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2">{getName(r.department)}</td>
                      <td className="px-4 py-2">{getName(r.hospital)}</td>
                      <td className="px-4 py-2 text-gray-500 text-xs">{r.start_date||'—'}</td>
                      <td className="px-4 py-2 text-gray-500 text-xs">{r.end_date||'—'}</td>
                      <td className="px-4 py-2"><span className={`px-2 py-0.5 rounded text-xs ${r.status==='approved'?'bg-green-50 text-green-700':r.status==='pending'?'bg-yellow-50 text-yellow-700':'bg-gray-50 text-gray-600'}`}>{r.status||'—'}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
    </ProtectedRoute>
  );
}
