import { redirect } from 'next/navigation';

export default function ResidentProgressRedirect() {
  redirect('/dashboard/resident');
  return null;
}
