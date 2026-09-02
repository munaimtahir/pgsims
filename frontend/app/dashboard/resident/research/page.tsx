import { redirect } from 'next/navigation';

export default function ResidentResearchRedirect() {
  redirect('/dashboard/resident');
  return null;
}
