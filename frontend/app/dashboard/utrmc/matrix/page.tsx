'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseHospital, UserbaseDepartment, UserbaseHospitalDepartment } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

export default function MatrixPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  const [hospitals, setHospitals] = useState<UserbaseHospital[]>([]);
  const [departments, setDepartments] = useState<UserbaseDepartment[]>([]);
  const [matrix, setMatrix] = useState<UserbaseHospitalDepartment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [toggling, setToggling] = useState<string | null>(null);

  const load = () => Promise.all([
    userbaseApi.hospitals.list(),
    userbaseApi.departments.list(),
    userbaseApi.matrix.list(),
  ]).then(([h, d, m]) => { setHospitals(h); setDepartments(d); setMatrix(m); })
    .catch(() => setError('Failed to load'))
    .finally(() => setLoading(false));

  useEffect(() => { load(); }, []);

  const getCellEntry = (hId: number, dId: number) =>
    matrix.find(m => {
      const hIdM = typeof m.hospital === 'object' ? m.hospital.id : (m.hospital_id ?? m.hospital);
      const dIdM = typeof m.department === 'object' ? m.department.id : (m.department_id ?? m.department);
      return hIdM === hId && dIdM === dId;
    });

  const toggle = async (hId: number, dId: number) => {
    const key = `${hId}-${dId}`;
    const existing = getCellEntry(hId, dId);
    setToggling(key);
    try {
      if (existing) {
        if (existing.active) await userbaseApi.matrix.update(existing.id, { active: false });
        else await userbaseApi.matrix.update(existing.id, { active: true });
      } else {
        await userbaseApi.matrix.create({ hospital_id: hId, department_id: dId, active: true });
      }
      await load();
    } catch { setError('Toggle failed'); }
    finally { setToggling(null); }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Hospital–Department Matrix</h1>
      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="overflow-auto">
        <table className="text-xs border-collapse">
          <thead>
            <tr>
              <th className="border border-gray-200 px-2 py-1 bg-gray-50 text-left min-w-32">Hospital \ Dept</th>
              {departments.map(d => (
                <th key={d.id} className="border border-gray-200 px-2 py-1 bg-gray-50 text-center max-w-20 truncate" title={d.name}>{d.code}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {hospitals.map(h => (
              <tr key={h.id}>
                <td className="border border-gray-200 px-2 py-1 font-medium bg-gray-50">{h.name}</td>
                {departments.map(d => {
                  const entry = getCellEntry(h.id, d.id);
                  const active = entry?.active ?? false;
                  const key = `${h.id}-${d.id}`;
                  return (
                    <td key={d.id} className="border border-gray-200 px-2 py-1 text-center">
                      <button
                        onClick={() => toggle(h.id, d.id)}
                        disabled={!canManage || toggling === key}
                        className={`w-5 h-5 rounded border-2 text-xs ${active ? 'bg-indigo-600 border-indigo-600 text-white' : 'bg-white border-gray-300'} disabled:opacity-40`}
                        title={
                          canManage
                            ? active ? 'Active - click to deactivate' : 'Inactive - click to activate'
                            : active ? 'Active (read-only)' : 'Inactive (read-only)'
                        }
                      >
                        {active ? '✓' : ''}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
