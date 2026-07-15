import { redirect } from 'next/navigation';

export default function UtrmcBackupRedirect() {
  redirect('/dashboard/utrmc');
  return null;
}
