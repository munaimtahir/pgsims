'use client';
import { useEffect, useState } from 'react';
import ReadonlyNotice from '@/components/ReadonlyNotice';
import PageHeader from '@/components/ui/PageHeader';
import { useAuthStore } from '@/store/authStore';
import { userbaseApi, UserbaseStaffProfile } from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';

interface SupervisorRow {
  userId: number;
  username: string;
  name: string;
  email: string;
  role: string;
  specialty: string;
  designation: string;
  phone: string;
  active: boolean;
}

interface SupervisorForm {
  email: string;
  first_name: string;
  last_name: string;
  specialty: string;
  designation: string;
  phone: string;
  active: boolean;
  password?: string;
}

const SPECIALTY_OPTIONS = [
  { value: 'medicine', label: 'Internal Medicine' },
  { value: 'surgery', label: 'Surgery' },
  { value: 'pediatrics', label: 'Pediatrics' },
  { value: 'gynecology', label: 'Gynecology & Obstetrics' },
  { value: 'orthopedics', label: 'Orthopedics' },
  { value: 'cardiology', label: 'Cardiology' },
  { value: 'neurology', label: 'Neurology' },
  { value: 'urology', label: 'Urology' },
  { value: 'psychiatry', label: 'Psychiatry' },
  { value: 'dermatology', label: 'Dermatology' },
  { value: 'radiology', label: 'Radiology' },
  { value: 'anesthesia', label: 'Anesthesia' },
  { value: 'pathology', label: 'Pathology' },
  { value: 'microbiology', label: 'Microbiology' },
  { value: 'pharmacology', label: 'Pharmacology' },
  { value: 'community_medicine', label: 'Community Medicine' },
  { value: 'forensic_medicine', label: 'Forensic Medicine' },
  { value: 'other', label: 'Other' },
];

function getErrorMessage(error: unknown, fallback = 'Action failed'): string {
  if (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof (error as { response?: unknown }).response === 'object' &&
    (error as { response?: unknown }).response !== null &&
    'data' in ((error as { response?: { data?: unknown } }).response || {})
  ) {
    const data = (error as { response?: { data?: unknown } }).response?.data;
    if (typeof data === 'object' && data !== null) {
      return JSON.stringify(data);
    }
    return String(data);
  }
  return fallback;
}

export default function SupervisorsPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);
  
  const [rows, setRows] = useState<SupervisorRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<SupervisorRow | null>(null);
  const [form, setForm] = useState<SupervisorForm>({
    email: '',
    first_name: '',
    last_name: '',
    specialty: '',
    designation: '',
    phone: '',
    active: true,
    password: '',
  });
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [usersData, staffData] = await Promise.all([
        userbaseApi.users.list(),
        userbaseApi.staff.list(),
      ]);

      const staffMap = new Map<number, UserbaseStaffProfile>();
      staffData.forEach((s) => {
        if (s.user?.id) {
          staffMap.set(s.user.id, s);
        }
      });

      const joined: SupervisorRow[] = usersData
        .filter((u) => u.role === 'supervisor' || u.role === 'faculty')
        .map((u) => {
          const profile = staffMap.get(u.id);
          return {
            userId: u.id,
            username: u.username,
            name: u.full_name || `${u.first_name} ${u.last_name}`.trim(),
            email: u.email || '',
            role: u.role,
            specialty: u.specialty || '',
            designation: profile?.designation || '',
            phone: profile?.phone || '',
            active: profile ? profile.active : u.is_active,
          };
        });

      setRows(joined);
    } catch {
      setError('Failed to load supervisor data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const openEdit = (row: SupervisorRow) => {
    const spaceIndex = row.name.indexOf(' ');
    const first = spaceIndex > 0 ? row.name.slice(0, spaceIndex) : row.name;
    const last = spaceIndex > 0 ? row.name.slice(spaceIndex + 1) : '';

    setForm({
      email: row.email,
      first_name: first,
      last_name: last,
      specialty: row.specialty,
      designation: row.designation,
      phone: row.phone,
      active: row.active,
      password: '',
    });
    setEditing(row);
    setShowModal(true);
  };

  const save = async () => {
    if (!editing) return;
    setSaving(true);
    setError('');
    try {
      const userPayload: Record<string, any> = {
        email: form.email,
        first_name: form.first_name,
        last_name: form.last_name,
        specialty: form.specialty,
      };
      if (form.password) {
        userPayload.password = form.password;
      }
      await userbaseApi.users.update(editing.userId, userPayload);

      await userbaseApi.staff.update(editing.userId, {
        designation: form.designation,
        phone: form.phone,
        active: form.active,
      });

      setShowModal(false);
      load();
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Failed to save changes.'));
    } finally {
      setSaving(false);
    }
  };

  const filtered = rows.filter(
    (r) =>
      !search ||
      r.username.toLowerCase().includes(search.toLowerCase()) ||
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      r.email.toLowerCase().includes(search.toLowerCase()) ||
      r.designation.toLowerCase().includes(search.toLowerCase())
  );

  const isEmpty = filtered.length === 0;

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="pg-page">
      <PageHeader
        title="Supervisors & Faculty"
        description="Manage designation, specialty, and contact details for supervisory staff."
      />
      {isReadonly && <ReadonlyNotice />}
      {error && (
        <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          {error}
        </div>
      )}
      <div className="mb-4">
        <label className="pg-form-label" htmlFor="search-supervisors">
          Search supervisors
        </label>
        <input
          id="search-supervisors"
          className="pg-form-input w-full sm:w-96"
          placeholder="Search by name, username, email, or designation"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {isEmpty ? (
        <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-6 text-sm leading-6 text-slate-600">
          No supervisors or faculty match this search.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                {[
                  'Username',
                  'Name',
                  'Email',
                  'Specialty',
                  'Designation',
                  'Phone',
                  'Active',
                  'Actions',
                ].map((h) => (
                  <th
                    key={h}
                    className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map((r) => (
                <tr key={r.userId} className="hover:bg-gray-50">
                  <td className="px-3 py-3 font-medium text-gray-900">{r.username}</td>
                  <td className="px-3 py-3">{r.name}</td>
                  <td className="px-3 py-3 text-xs text-gray-500">{r.email || '—'}</td>
                  <td className="px-3 py-3 text-xs capitalize">{r.specialty || '—'}</td>
                  <td className="px-3 py-3 text-xs">{r.designation || '—'}</td>
                  <td className="px-3 py-3 text-xs text-gray-500">{r.phone || '—'}</td>
                  <td className="px-3 py-3">
                    {r.active ? (
                      <span className="text-green-600 text-xs">Yes</span>
                    ) : (
                      <span className="text-gray-400 text-xs">No</span>
                    )}
                  </td>
                  <td className="px-3 py-3">
                    {canManage ? (
                      <button
                        onClick={() => openEdit(r)}
                        className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700"
                      >
                        Edit
                      </button>
                    ) : (
                      <span className="text-xs text-gray-400">View only</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && editing && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 px-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-semibold mb-4">Edit {editing.name}</h2>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="pg-form-label" htmlFor="first_name">First Name</label>
                  <input
                    id="first_name"
                    className="pg-form-input"
                    value={form.first_name}
                    onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="pg-form-label" htmlFor="last_name">Last Name</label>
                  <input
                    id="last_name"
                    className="pg-form-input"
                    value={form.last_name}
                    onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  />
                </div>
              </div>
              <div>
                <label className="pg-form-label" htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  className="pg-form-input"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div>
                <label className="pg-form-label" htmlFor="specialty">Specialty</label>
                <select
                  id="specialty"
                  className="pg-form-input"
                  value={form.specialty}
                  onChange={(e) => setForm({ ...form, specialty: e.target.value })}
                >
                  <option value="">Select specialty</option>
                  {SPECIALTY_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="pg-form-label" htmlFor="designation">Designation</label>
                <input
                  id="designation"
                  className="pg-form-input"
                  value={form.designation}
                  onChange={(e) => setForm({ ...form, designation: e.target.value })}
                />
              </div>
              <div>
                <label className="pg-form-label" htmlFor="phone">Phone Number</label>
                <input
                  id="phone"
                  className="pg-form-input"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
              </div>
              <div>
                <label className="pg-form-label" htmlFor="supervisor-password">New Password (leave blank to keep current)</label>
                <input
                  id="supervisor-password"
                  type="password"
                  className="pg-form-input"
                  value={form.password || ''}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                />
              </div>
              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="active-check"
                  checked={form.active}
                  onChange={(e) => setForm({ ...form, active: e.target.checked })}
                />
                <label htmlFor="active-check" className="text-sm font-medium">
                  Active Staff Member
                </label>
              </div>
            </div>

            <div className="mt-5 flex gap-2 justify-end">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-sm border rounded"
              >
                Cancel
              </button>
              <button
                onClick={save}
                disabled={saving}
                className="pg-btn-primary"
              >
                {saving ? 'Saving...' : 'Save'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
