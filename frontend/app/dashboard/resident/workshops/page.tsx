import { redirect } from 'next/navigation';

export default function ResidentWorkshopsRedirect() {
  redirect('/dashboard/resident');
  return null;
}
