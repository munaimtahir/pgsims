'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import apiClient from '@/lib/api/client';

type DocumentRow = { id: number; title: string; stage: string; status: string; verification_remarks?: string; file?: string | null };

export default function ResidentDocumentsPage() {
  const [documents, setDocuments] = useState<DocumentRow[]>([]);
  const [error, setError] = useState('');
  const load = () => apiClient.get<DocumentRow[]>('/api/resident-documents/').then((r) => setDocuments(r.data)).catch(() => setError('Unable to load documents.'));
  useEffect(() => { load(); }, []);
  const defer = (id: number) => apiClient.post(`/api/resident-documents/${id}/defer/`).then(load);
  const upload = (id: number, file?: File) => { if (!file) return; const body = new FormData(); body.append('file', file); return apiClient.post(`/api/resident-documents/${id}/upload/`, body).then(load); };
  return <ProtectedRoute allowedRoles={['RESIDENT']}><div className="pg-page space-y-6"><PageHeader title="My Documents" description="Upload required documents now or defer them without blocking dashboard access." />{error && <p className="text-sm text-red-600">{error}</p>}<div className="grid gap-4 md:grid-cols-2">{documents.map((doc) => <section className="pg-card" key={doc.id}><h2 className="font-semibold">{doc.title}</h2><p className="mt-1 text-sm text-slate-500">{doc.stage === 'ONBOARDING' ? 'Required for onboarding' : doc.stage === 'DURING_TRAINING' ? 'Required later' : 'Optional'}</p><p className="mt-2 text-sm">Status: <span className="font-medium">{doc.status.replaceAll('_', ' ')}</span></p>{doc.verification_remarks && <p className="mt-2 text-sm text-amber-700">Reason: {doc.verification_remarks}</p>}<div className="mt-4 flex flex-wrap gap-2"><label className="pg-button cursor-pointer"><input type="file" className="hidden" onChange={(e) => upload(doc.id, e.target.files?.[0])} />{doc.status === 'DEFERRED' || doc.status === 'REUPLOAD_REQUIRED' ? 'Upload Now' : 'Upload / Replace'}</label>{doc.status === 'NOT_STARTED' && <button className="pg-button-secondary" onClick={() => defer(doc.id)}>Upload Later</button>}</div></section>)}</div></div></ProtectedRoute>;
}
