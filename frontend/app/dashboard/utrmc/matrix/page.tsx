'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
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
  const [search, setSearch] = useState('');

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

  const searchValue = search.trim().toLowerCase();
  const filteredHospitals = hospitals.filter((hospital) => {
    if (!searchValue) {
      return true;
    }
    return hospital.name.toLowerCase().includes(searchValue) || hospital.code.toLowerCase().includes(searchValue);
  });
  const filteredDepartments = departments.filter((department) => {
    if (!searchValue) {
      return true;
    }
    return department.name.toLowerCase().includes(searchValue) || department.code.toLowerCase().includes(searchValue);
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
    <div className="pg-page">
      <PageHeader
        title="Hospital–Department Matrix"
        description="Search and manage the active hospital/department relationships used in rotation placement."
      />
      {isReadonly && <ReadonlyNotice />}
      {error && <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">{error}</div>}
      <div className="mb-4">
        <label className="pg-form-label" htmlFor="matrix-search">Search hospitals or departments</label>
        <input
          id="matrix-search"
          className="pg-form-input w-full sm:w-96"
          placeholder="Filter by hospital code, department code, or name"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>
      <div className="mb-4 flex flex-wrap gap-2 text-xs text-slate-500">
        <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1">Active</span>
        <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1">Inactive</span>
        <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1">Click to toggle when enabled</span>
      </div>
      {filteredHospitals.length === 0 || filteredDepartments.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
          No hospital/department combinations match the current search.
        </div>
      ) : (
        <div className="overflow-auto rounded-xl border border-gray-200 bg-white p-3">
          <table className="text-xs border-collapse">
            <thead>
              <tr>
                <th className="min-w-40 border border-gray-200 bg-gray-50 px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-gray-600">
                  Hospital \ Dept
                </th>
                {filteredDepartments.map((department) => (
                  <th
                    key={department.id}
                    className="max-w-24 border border-gray-200 bg-gray-50 px-3 py-2 text-center text-[11px] font-semibold uppercase tracking-wider text-gray-600"
                    title={`${department.name} (${department.code})`}
                  >
                    {department.code}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredHospitals.map((hospital) => (
                <tr key={hospital.id}>
                  <td className="border border-gray-200 bg-gray-50 px-3 py-3 font-medium text-gray-900">
                    <div className="leading-5">
                      <p>{hospital.name}</p>
                      <p className="text-[11px] font-normal text-gray-500">{hospital.code}</p>
                    </div>
                  </td>
                  {filteredDepartments.map((department) => {
                    const entry = getCellEntry(hospital.id, department.id);
                    const active = entry?.active ?? false;
                    const key = `${hospital.id}-${department.id}`;
                    return (
                      <td key={department.id} className="border border-gray-200 px-3 py-3 text-center">
                        <button
                          onClick={() => toggle(hospital.id, department.id)}
                          disabled={!canManage || toggling === key}
                          className={`inline-flex h-8 w-8 items-center justify-center rounded-full border-2 text-xs font-semibold ${
                            active ? 'bg-indigo-600 border-indigo-600 text-white' : 'bg-white border-gray-300 text-gray-500'
                          } disabled:opacity-40`}
                          title={
                            canManage
                              ? active
                                ? 'Active - click to deactivate'
                                : 'Inactive - click to activate'
                              : active
                                ? 'Active (read-only)'
                                : 'Inactive (read-only)'
                          }
                          aria-label={`${hospital.name} and ${department.name} ${active ? 'active' : 'inactive'}`}
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
      )}
    </div>
  );
}
