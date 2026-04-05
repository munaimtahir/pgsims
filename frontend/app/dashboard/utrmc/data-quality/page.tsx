'use client';

import { useEffect, useMemo, useState } from 'react';

import ReadonlyNotice from '@/components/ReadonlyNotice';
import {
  DataCorrectionAuditRow,
  DataQualitySummary,
  DataQualityUserRow,
  userbaseApi,
} from '@/lib/api/userbase';
import { isUtrmcManagerRole, isUtrmcReadonlyRole } from '@/lib/rbac';
import { useAuthStore } from '@/store/authStore';

const FILTERS: Array<{ key: string; label: string }> = [
  { key: '', label: 'All' },
  { key: 'incomplete_profile', label: 'Incomplete Profiles' },
  { key: 'placeholder_email', label: 'Placeholder Emails' },
  { key: 'missing_dates', label: 'Missing Dates' },
  { key: 'missing_email', label: 'Missing Emails' },
];

const ISSUE_LABELS: Record<string, string> = {
  missing_email: 'Missing Email',
  placeholder_email: 'Placeholder Email',
  missing_year: 'Missing Year',
  missing_resident_profile: 'Missing Resident Profile',
  missing_training_start: 'Missing Training Start',
  default_training_start: 'Default Training Start',
  invalid_training_end: 'Invalid Training End',
  missing_training_dates: 'Missing Training Dates',
  missing_supervision_dates: 'Missing Supervision Dates',
};

type EditState = {
  userId: number;
  name: string;
  email: string;
  year: string;
  training_start: string;
  training_end: string;
  training_level: string;
};

const EMPTY_SUMMARY: DataQualitySummary = {
  total_users: 0,
  users_with_placeholder_email: 0,
  users_with_missing_dates: 0,
  complete_profiles: 0,
  incomplete_profiles: 0,
};

function normalizeIssue(issue: string): string {
  return ISSUE_LABELS[issue] || issue.replaceAll('_', ' ');
}

export default function DataQualityPage() {
  const { user } = useAuthStore();
  const canManage = isUtrmcManagerRole(user?.role);
  const isReadonly = isUtrmcReadonlyRole(user?.role);

  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<DataQualitySummary>(EMPTY_SUMMARY);
  const [rows, setRows] = useState<DataQualityUserRow[]>([]);
  const [audit, setAudit] = useState<DataCorrectionAuditRow[]>([]);
  const [activeFilter, setActiveFilter] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [saving, setSaving] = useState(false);
  const [edit, setEdit] = useState<EditState | null>(null);

  const flash = (text: string, isError = false) => {
    if (isError) {
      setError(text);
    } else {
      setMessage(text);
    }
    window.setTimeout(() => {
      setError('');
      setMessage('');
    }, 4000);
  };

  const load = async (filterValue = activeFilter) => {
    setLoading(true);
    setError('');
    try {
      const [summaryData, userRows, auditRows] = await Promise.all([
        userbaseApi.dataQuality.summary(),
        userbaseApi.dataQuality.users(filterValue || undefined),
        userbaseApi.dataQuality.audit(),
      ]);
      setSummary(summaryData);
      setRows(userRows);
      setAudit(auditRows);
    } catch {
      setError('Failed to load data quality dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      return;
    }
    load('');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const openEdit = (row: DataQualityUserRow) => {
    setEdit({
      userId: row.id,
      name: row.name,
      email: row.email || '',
      year: row.year || '',
      training_start: '',
      training_end: '',
      training_level: '',
    });
  };

  const saveEdit = async () => {
    if (!edit || !canManage) {
      return;
    }
    setSaving(true);
    setError('');

    try {
      await userbaseApi.users.update(edit.userId, {
        email: edit.email,
        year: edit.year || undefined,
      });

      const residentPayload: Record<string, string> = {};
      if (edit.training_start) {
        residentPayload.training_start = edit.training_start;
      }
      if (edit.training_end) {
        residentPayload.training_end = edit.training_end;
      }
      if (edit.training_level) {
        residentPayload.training_level = edit.training_level;
      }
      if (Object.keys(residentPayload).length > 0) {
        await userbaseApi.residents.update(edit.userId, residentPayload);
      }

      await userbaseApi.dataQuality.recompute();
      setEdit(null);
      flash('Resident correction saved.');
      await load(activeFilter);
    } catch {
      flash('Failed to save correction.', true);
    } finally {
      setSaving(false);
    }
  };

  const badgeClass = (issue: string): string => {
    if (issue.includes('placeholder') || issue.includes('invalid')) {
      return 'bg-red-100 text-red-700';
    }
    if (issue.includes('missing') || issue.includes('default')) {
      return 'bg-yellow-100 text-yellow-800';
    }
    return 'bg-gray-100 text-gray-700';
  };

  const summaryCards = useMemo(
    () => [
      { title: 'Total Residents', value: summary.total_users },
      { title: 'Incomplete Profiles', value: summary.incomplete_profiles },
      { title: 'Placeholder Emails', value: summary.users_with_placeholder_email },
      { title: 'Missing Dates', value: summary.users_with_missing_dates },
    ],
    [summary]
  );

  if (loading) {
    return <p className="text-gray-500">Loading data quality dashboard...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Data Quality Dashboard</h1>
        {canManage && (
          <button
            onClick={async () => {
              setSaving(true);
              try {
                await userbaseApi.dataQuality.recompute();
                flash('Data quality flags recomputed.');
                await load(activeFilter);
              } catch {
                flash('Recompute failed.', true);
              } finally {
                setSaving(false);
              }
            }}
            disabled={saving}
            className="px-4 py-2 bg-indigo-600 text-white rounded text-sm disabled:opacity-50"
          >
            {saving ? 'Working...' : 'Recompute Flags'}
          </button>
        )}
      </div>

      {isReadonly && <ReadonlyNotice />}
      {error && <p className="text-sm text-red-600">{error}</p>}
      {message && <p className="text-sm text-green-700">{message}</p>}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {summaryCards.map((card) => (
          <div key={card.title} className="rounded-lg border border-gray-200 bg-white p-4">
            <p className="text-sm text-gray-500">{card.title}</p>
            <p className="text-2xl font-semibold text-gray-900">{card.value}</p>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        {FILTERS.map((filterOption) => (
          <button
            key={filterOption.key}
            onClick={async () => {
              setActiveFilter(filterOption.key);
              await load(filterOption.key);
            }}
            className={`px-3 py-1.5 text-sm rounded border ${
              activeFilter === filterOption.key
                ? 'bg-indigo-600 text-white border-indigo-600'
                : 'bg-white text-gray-700 border-gray-300'
            }`}
          >
            {filterOption.label}
          </button>
        ))}
      </div>

      <div className="rounded-lg border border-gray-200 bg-white overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              {['Name', 'Email', 'Year', 'Supervisor', 'Issues', 'Status', 'Action'].map((h) => (
                <th key={h} className="text-left px-3 py-2 font-medium text-gray-600">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {rows.map((row) => (
              <tr key={row.id} className="hover:bg-gray-50">
                <td className="px-3 py-2">{row.name}</td>
                <td className="px-3 py-2 text-xs text-gray-600">{row.email || '-'}</td>
                <td className="px-3 py-2">{row.year || '-'}</td>
                <td className="px-3 py-2">{row.supervisor || '-'}</td>
                <td className="px-3 py-2">
                  <div className="flex gap-1 flex-wrap">
                    {(row.issues || []).map((issue) => (
                      <span
                        key={`${row.id}-${issue}`}
                        className={`px-2 py-0.5 rounded text-xs ${badgeClass(issue)}`}
                      >
                        {normalizeIssue(issue)}
                      </span>
                    ))}
                    {row.issues.length === 0 && <span className="text-gray-400 text-xs">No issues</span>}
                  </div>
                </td>
                <td className="px-3 py-2">
                  <span
                    className={`px-2 py-0.5 rounded text-xs ${
                      row.is_complete_profile ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}
                  >
                    {row.is_complete_profile ? 'Complete' : 'Incomplete'}
                  </span>
                </td>
                <td className="px-3 py-2">
                  {canManage ? (
                    <button onClick={() => openEdit(row)} className="text-indigo-600 hover:underline text-xs">
                      Edit
                    </button>
                  ) : (
                    <span className="text-gray-400 text-xs">View only</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">Recent Correction Audit</h2>
        <div className="space-y-2 max-h-72 overflow-auto">
          {audit.length === 0 && <p className="text-sm text-gray-400">No correction events yet.</p>}
          {audit.map((item) => (
            <div key={item.id} className="text-sm border border-gray-100 rounded p-2">
              <p className="text-gray-800">
                <span className="font-medium">{item.actor || 'System'}</span> changed{' '}
                <span className="font-medium">{item.entity_type}:{item.entity_id}</span> field{' '}
                <span className="font-medium">{item.field_name}</span>
              </p>
              <p className="text-xs text-gray-600">
                {item.old_value || '(empty)'} → {item.new_value || '(empty)'}
              </p>
            </div>
          ))}
        </div>
      </div>

      {edit && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Edit {edit.name}</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm text-gray-700 mb-1">Email</label>
                <input
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={edit.email}
                  onChange={(event) => setEdit({ ...edit, email: event.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm text-gray-700 mb-1">Training Year</label>
                <select
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={edit.year}
                  onChange={(event) => setEdit({ ...edit, year: event.target.value })}
                >
                  <option value="">Select year</option>
                  <option value="1">Year 1</option>
                  <option value="2">Year 2</option>
                  <option value="3">Year 3</option>
                  <option value="4">Year 4</option>
                  <option value="5">Year 5</option>
                </select>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-700 mb-1">Training Start (ISO)</label>
                  <input
                    type="date"
                    className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                    value={edit.training_start}
                    onChange={(event) => setEdit({ ...edit, training_start: event.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-700 mb-1">Training End (ISO)</label>
                  <input
                    type="date"
                    className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                    value={edit.training_end}
                    onChange={(event) => setEdit({ ...edit, training_end: event.target.value })}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-700 mb-1">Training Level</label>
                <input
                  className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                  value={edit.training_level}
                  onChange={(event) => setEdit({ ...edit, training_level: event.target.value })}
                />
              </div>
            </div>
            <div className="mt-5 flex justify-end gap-2">
              <button
                onClick={() => setEdit(null)}
                className="px-4 py-2 text-sm border border-gray-300 rounded"
              >
                Cancel
              </button>
              <button
                onClick={saveEdit}
                disabled={saving}
                className="px-4 py-2 text-sm bg-indigo-600 text-white rounded disabled:opacity-50"
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
