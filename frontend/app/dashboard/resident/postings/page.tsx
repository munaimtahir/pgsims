'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { trainingApi, DeputationPosting } from '@/lib/api/training';

const STATUS_COLORS: Record<string, string> = {
  SUBMITTED: 'bg-yellow-100 text-yellow-800',
  APPROVED: 'bg-green-100 text-green-800',
  REJECTED: 'bg-red-100 text-red-700',
  COMPLETED: 'bg-blue-100 text-blue-800',
};

const STATUS_LABELS: Record<string, string> = {
  SUBMITTED: 'Pending Approval',
  APPROVED: 'Approved',
  REJECTED: 'Rejected',
  COMPLETED: 'Completed',
};

interface PostingForm {
  posting_type: string;
  institution_name: string;
  city: string;
  start_date: string;
  end_date: string;
  notes: string;
}

const EMPTY_FORM: PostingForm = {
  posting_type: 'off_service',
  institution_name: '',
  city: '',
  start_date: '',
  end_date: '',
  notes: '',
};

export default function ResidentPostingsPage() {
  const [trainingRecordId, setTrainingRecordId] = useState<number | null>(null);
  const [postings, setPostings] = useState<DeputationPosting[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<PostingForm>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const load = () => {
    setLoading(true);
    Promise.all([
      trainingApi.listPostings(),
      trainingApi.getResidentSummary(),
    ])
      .then(([nextPostings, summary]) => {
        setPostings(nextPostings);
        setTrainingRecordId(summary.training_record.id);
      })
      .catch(() => setError('Failed to load postings.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const flash = (msg: string, isErr = false) => {
    if (isErr) { setError(msg); } else { setSuccess(msg); }
    setTimeout(() => { setError(''); setSuccess(''); }, 4000);
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.institution_name || !form.start_date || !form.end_date) return;
    if (!trainingRecordId) {
      flash('Training record is not available for posting requests yet.', true);
      return;
    }
    setSaving(true);
    setError('');
    try {
      await trainingApi.createPosting({
        ...form,
        resident_training: trainingRecordId,
      });
      setShowForm(false);
      setForm(EMPTY_FORM);
      flash('Posting request submitted for review.');
      load();
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      flash(msg || 'Failed to create posting.', true);
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute allowedRoles={['pg', 'resident']}>
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Deputation Postings</h1>
            <p className="text-sm text-gray-500 mt-1">Off-service rotations and external placements</p>
          </div>
          <button
            onClick={() => { setShowForm(true); setForm(EMPTY_FORM); }}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700"
          >
            + Request Posting
          </button>
        </div>

        {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{error}</div>}
        {success && <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700">{success}</div>}

        {/* Create form */}
        {showForm && (
          <form onSubmit={handleCreate} className="bg-white border border-gray-200 rounded-xl p-5 mb-6 shadow-sm space-y-4">
            <h2 className="font-semibold text-gray-800">New Posting Request</h2>
            <p className="text-sm text-gray-500">
              Posting requests are submitted immediately after creation and then reviewed by UTRMC.
            </p>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select
                  value={form.posting_type}
                  onChange={(e) => setForm({ ...form, posting_type: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                >
                  <option value="off_service">Off-Service</option>
                  <option value="deputation">Deputation</option>
                  <option value="exchange">Exchange Programme</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">City / Location</label>
                <input
                  type="text"
                  value={form.city}
                  onChange={(e) => setForm({ ...form, city: e.target.value })}
                  placeholder="e.g. Riyadh"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Institution / Hospital Name *</label>
              <input
                required
                type="text"
                value={form.institution_name}
                onChange={(e) => setForm({ ...form, institution_name: e.target.value })}
                placeholder="Name of the hosting institution"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Start Date *</label>
                <input
                  required
                  type="date"
                  value={form.start_date}
                  onChange={(e) => setForm({ ...form, start_date: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">End Date *</label>
                <input
                  required
                  type="date"
                  value={form.end_date}
                  onChange={(e) => setForm({ ...form, end_date: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notes / Purpose</label>
              <textarea
                rows={2}
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                placeholder="Optional — reason or clinical objectives for this posting"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                {saving ? 'Saving…' : 'Create Request'}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {loading && <p className="text-gray-400 text-sm">Loading…</p>}

        {!loading && postings.length === 0 && !showForm && (
          <div className="text-center py-16 border-2 border-dashed border-gray-200 rounded-xl">
            <p className="text-gray-500 font-medium">No postings yet</p>
            <p className="text-sm text-gray-400 mt-1">Request a deputation or off-service placement above.</p>
          </div>
        )}

        <div className="space-y-4">
          {postings.map((posting) => (
            <div key={posting.id} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${STATUS_COLORS[posting.status] ?? 'bg-gray-100 text-gray-600'}`}>
                      {STATUS_LABELS[posting.status] ?? posting.status}
                    </span>
                    <span className="text-xs text-gray-400 uppercase tracking-wide">{posting.posting_type || 'Deputation'}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900">{posting.institution_name}</h3>
                  {posting.city && <p className="text-sm text-gray-500">{posting.city}</p>}
                  <p className="text-sm text-gray-500 mt-1">
                    📅 {posting.start_date} → {posting.end_date}
                  </p>
                  {posting.notes && (
                    <p className="text-sm text-gray-500 mt-1 italic">{posting.notes}</p>
                  )}
                  {posting.status === 'REJECTED' && posting.reject_reason && (
                    <p className="text-sm text-red-600 mt-2">
                      <span className="font-medium">Reason:</span> {posting.reject_reason}
                    </p>
                  )}
                  {posting.approved_at && (
                    <p className="text-xs text-gray-400 mt-1">
                      ✓ Approved {new Date(posting.approved_at).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
