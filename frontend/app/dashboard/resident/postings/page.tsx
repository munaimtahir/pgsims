import { redirect } from 'next/navigation';

export default function ResidentPostingsRedirect() {
  redirect('/dashboard/resident');
  return null;
}
