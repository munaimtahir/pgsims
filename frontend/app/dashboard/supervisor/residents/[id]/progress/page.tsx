import { redirect } from 'next/navigation';

export default function SupervisorResidentProgressRedirect() {
  redirect('/dashboard/supervisor');
  return null;
}
