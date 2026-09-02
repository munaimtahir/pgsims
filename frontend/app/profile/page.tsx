'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import PageHeader from '@/components/ui/PageHeader';
import authApi, { AuthMeResponse } from '@/lib/api/auth';

export default function ProfilePage() {
  const [state, setState] = useState<AuthMeResponse | null>(null);
  useEffect(() => { authApi.me().then(setState); }, []);
  return <ProtectedRoute><div className="pg-page space-y-6"><PageHeader title="My Profile" description="Your account and profile completion state." />{state && <section className="pg-card space-y-2 text-sm"><p>Username: {state.username}</p><p>Role: {state.role}</p><p>Profile status: {state.profile_status}</p><p>Profile information complete: {state.is_profile_complete ? 'Yes' : 'No'}</p>{!state.is_profile_complete && <a className="underline" href="/complete-profile">Complete required profile information</a>}</section>}</div></ProtectedRoute>;
}
