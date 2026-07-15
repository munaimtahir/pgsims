import { redirect } from 'next/navigation';

export default function PgDepartmentRosterRedirect() {
  redirect('/dashboard/resident');
  return null;
}
