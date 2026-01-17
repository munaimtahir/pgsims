'use client';

import { useCallback, useEffect, useState } from 'react';
import { format } from 'date-fns';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardLayout from '@/components/layout/DashboardLayout';
import ErrorBanner from '@/components/ui/ErrorBanner';
import EmptyState from '@/components/ui/EmptyState';
import SectionCard from '@/components/ui/SectionCard';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { TableSkeleton } from '@/components/ui/LoadingSkeleton';
import DataTable, { Column } from '@/components/ui/DataTable';
import { logbookApi, LogbookEntry, PGLogbookEntryPayload } from '@/lib/api';

const emptyForm: PGLogbookEntryPayload = {
  case_title: '',
  date: '',
  location_of_activity: '',
  patient_history_summary: '',
  management_action: '',
  topic_subtopic: '',
};

const normalizeEntries = (data: { results?: LogbookEntry[] } | LogbookEntry[]) => {
  if (Array.isArray(data)) {
    return data;
  }
  return data.results ?? [];
};

const statusClasses: Record<LogbookEntry['status'], string> = {
  draft: 'bg-gray-100 text-gray-800',
  pending: 'bg-yellow-100 text-yellow-800',
  approved: 'bg-green-100 text-green-800',
  returned: 'bg-orange-100 text-orange-800',
  rejected: 'bg-red-100 text-red-800',
  archived: 'bg-gray-100 text-gray-800',
};

export default function PGLogbookPage() {
  const [entries, setEntries] = useState<LogbookEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [formData, setFormData] = useState<PGLogbookEntryPayload>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const [submittingId, setSubmittingId] = useState<number | null>(null);

  const loadEntries = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await logbookApi.getMyEntries();
      setEntries(normalizeEntries(data));
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load logbook entries';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadEntries();
  }, [loadEntries]);

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleEdit = (entry: LogbookEntry) => {
    setEditingId(entry.id);
    setFormData({
      case_title: entry.case_title || '',
      date: entry.date || '',
      location_of_activity: entry.location_of_activity || '',
      patient_history_summary: entry.patient_history_summary || '',
      management_action: entry.management_action || '',
      topic_subtopic: entry.topic_subtopic || '',
    });
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setFormData(emptyForm);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      setSaving(true);
      setError(null);
      if (editingId) {
        await logbookApi.updateMyEntry(editingId, formData);
        setSuccess('Draft logbook entry updated successfully.');
      } else {
        await logbookApi.createMyEntry(formData);
        setSuccess('Draft logbook entry created successfully.');
      }
      setFormData(emptyForm);
      setEditingId(null);
      loadEntries();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to save logbook entry';
      setError(message);
    } finally {
      setSaving(false);
    }
  };

  const handleSubmitEntry = async (entryId: number) => {
    if (!confirm('Submit this entry for supervisor review?')) {
      return;
    }

    try {
      setSubmittingId(entryId);
      setError(null);
      await logbookApi.submitMyEntry(entryId);
      setSuccess('Logbook entry submitted for supervisor review.');
      loadEntries();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to submit logbook entry';
      setError(message);
    } finally {
      setSubmittingId(null);
    }
  };

  const columns: Column<LogbookEntry>[] = [
    {
      key: 'date',
      label: 'Date',
      render: (item) => {
        try {
          return format(new Date(item.date), 'MMM dd, yyyy');
        } catch {
          return item.date || '-';
        }
      },
    },
    {
      key: 'case_title',
      label: 'Title/Type',
      render: (item) => item.case_title || '-',
    },
    {
      key: 'status',
      label: 'Status',
      render: (item) => {
        const className = statusClasses[item.status] || 'bg-gray-100 text-gray-800';
        return (
          <span className={`px-2 py-1 text-xs rounded-full ${className}`}>
            {item.status}
          </span>
        );
      },
    },
    {
      key: 'updated_at',
      label: 'Updated',
      render: (item) => {
        if (!item.updated_at) {
          return '-';
        }
        try {
          return format(new Date(item.updated_at), 'MMM dd, yyyy');
        } catch {
          return item.updated_at;
        }
      },
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (item) => (
        <div className="flex flex-wrap gap-2">
          {item.status === 'draft' && (
            <button
              type="button"
              onClick={() => handleEdit(item)}
              className="text-sm text-indigo-600 hover:text-indigo-900"
            >
              Edit
            </button>
          )}
          {item.status === 'draft' && (
            <button
              type="button"
              onClick={() => handleSubmitEntry(item.id)}
              disabled={submittingId === item.id}
              className="text-sm text-green-600 hover:text-green-900 disabled:opacity-50"
            >
              {submittingId === item.id ? 'Submitting...' : 'Submit'}
            </button>
          )}
        </div>
      ),
    },
  ];

  return (
    <ProtectedRoute allowedRoles={['pg']}>
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Logbook</h1>
            <p className="mt-2 text-gray-600">Manage your logbook entries</p>
          </div>

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
          {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

          <SectionCard title={editingId ? 'Edit Draft Entry' : 'Create Draft Entry'}>
            <form className="space-y-4" onSubmit={handleSubmit}>
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label htmlFor="case_title" className="block text-sm font-medium text-gray-700">
                    Case title
                  </label>
                  <input
                    type="text"
                    id="case_title"
                    name="case_title"
                    value={formData.case_title}
                    onChange={handleChange}
                    required
                    aria-required="true"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                    Date
                  </label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                    aria-required="true"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
                </div>
                <div className="sm:col-span-2">
                  <label htmlFor="location_of_activity" className="block text-sm font-medium text-gray-700">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location_of_activity"
                    name="location_of_activity"
                    value={formData.location_of_activity}
                    onChange={handleChange}
                    required
                    aria-required="true"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="patient_history_summary" className="block text-sm font-medium text-gray-700">
                  Patient history summary
                </label>
                <textarea
                  id="patient_history_summary"
                  name="patient_history_summary"
                  value={formData.patient_history_summary}
                  onChange={handleChange}
                  required
                  aria-required="true"
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div>
                <label htmlFor="management_action" className="block text-sm font-medium text-gray-700">
                  Management action
                </label>
                <textarea
                  id="management_action"
                  name="management_action"
                  value={formData.management_action}
                  onChange={handleChange}
                  required
                  aria-required="true"
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div>
                <label htmlFor="topic_subtopic" className="block text-sm font-medium text-gray-700">
                  Topic / subtopic
                </label>
                <input
                  type="text"
                  id="topic_subtopic"
                  name="topic_subtopic"
                  value={formData.topic_subtopic}
                  onChange={handleChange}
                  required
                  aria-required="true"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div className="flex flex-wrap gap-3">
                <button
                  type="submit"
                  disabled={saving}
                  className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 disabled:opacity-60"
                >
                  {saving ? 'Saving...' : editingId ? 'Update Draft' : 'Create Draft'}
                </button>
                {editingId && (
                  <button
                    type="button"
                    onClick={handleCancelEdit}
                    className="inline-flex items-center rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
                  >
                    Cancel edit
                  </button>
                )}
              </div>
            </form>
          </SectionCard>

          <SectionCard title="Logbook Entries">
            {loading ? (
              <TableSkeleton rows={8} cols={5} />
            ) : entries.length === 0 ? (
              <EmptyState
                title="No logbook entries yet"
                description="Create a draft entry to start tracking your clinical cases."
              />
            ) : (
              <DataTable columns={columns} data={entries} emptyMessage="No logbook entries found" />
            )}
          </SectionCard>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
