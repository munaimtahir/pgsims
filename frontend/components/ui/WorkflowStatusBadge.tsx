const STATUS_COLORS: Record<string, string> = {
  ELIGIBLE: 'bg-green-100 text-green-800 border-green-200',
  PARTIALLY_READY: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  NOT_READY: 'bg-red-100 text-red-800 border-red-200',
  ACTIVE: 'bg-blue-100 text-blue-800 border-blue-200',
  APPROVED: 'bg-green-100 text-green-800 border-green-200',
  SUBMITTED: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  DRAFT: 'bg-slate-100 text-slate-700 border-slate-200',
  RETURNED: 'bg-orange-100 text-orange-800 border-orange-200',
  REJECTED: 'bg-red-100 text-red-800 border-red-200',
  UNDER_REVIEW: 'bg-blue-100 text-blue-800 border-blue-200',
  CERTIFICATE_ISSUED: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  SUBMITTED_TO_SUPERVISOR: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  APPROVED_BY_SUPERVISOR: 'bg-green-100 text-green-800 border-green-200',
  SUBMITTED_TO_UNIVERSITY: 'bg-blue-100 text-blue-800 border-blue-200',
  ACCEPTED_BY_UNIVERSITY: 'bg-green-100 text-green-800 border-green-200',
  NOT_STARTED: 'bg-slate-100 text-slate-600 border-slate-200',
  IN_PROGRESS: 'bg-blue-100 text-blue-800 border-blue-200',
  SUBMITTED_THESIS: 'bg-green-100 text-green-800 border-green-200',
  PENDING_UTRMC_VERIFICATION: 'bg-violet-100 text-violet-800 border-violet-200',
};

function normalizeStatus(status: string | null | undefined): string | null {
  if (!status) {
    return null;
  }
  const normalized = status.trim().replace(/[-\s]+/g, '_').toUpperCase();
  return normalized || null;
}

export function formatStatusLabel(status: string | null | undefined) {
  if (!status) {
    return '—';
  }
  return status.replace(/_/g, ' ').trim();
}

export default function WorkflowStatusBadge({
  status,
  label,
  className = '',
}: {
  status: string | null | undefined;
  label?: string;
  className?: string;
}) {
  const normalized = normalizeStatus(status);
  if (!normalized) {
    return (
      <span className={`inline-flex rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500 ${className}`}>
        —
      </span>
    );
  }
  const cls = STATUS_COLORS[normalized] || 'bg-slate-100 text-slate-700 border-slate-200';
  return (
    <span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-medium ${cls} ${className}`}>
      {label || formatStatusLabel(normalized)}
    </span>
  );
}
