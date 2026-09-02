import { redirect } from 'next/navigation';

export default function SupervisorResearchApprovalsRedirect() {
  redirect('/dashboard/supervisor');
  return null;
}
