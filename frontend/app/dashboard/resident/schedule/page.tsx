import { redirect } from 'next/navigation';

export default function ResidentScheduleRedirect() {
  redirect('/dashboard/resident');
  return null;
}
