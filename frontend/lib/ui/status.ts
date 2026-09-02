export type BackendStatus =
  | 'draft'
  | 'pending'
  | 'returned'
  | 'rejected'
  | 'approved'
  | 'archived'
  | string;

export function getStatusLabel(status?: BackendStatus | null): string {
  switch (status) {
    case 'pending':
      return 'Submitted';
    case 'returned':
      return 'Returned';
    case 'rejected':
      return 'Rejected';
    case 'approved':
      return 'Approved';
    case 'draft':
      return 'Draft';
    case 'archived':
      return 'Archived';
    default:
      return status || 'Unknown';
  }
}

export function getStatusBadgeClass(status?: BackendStatus | null): string {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'returned':
      return 'bg-orange-100 text-orange-800';
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    case 'draft':
    case 'archived':
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

