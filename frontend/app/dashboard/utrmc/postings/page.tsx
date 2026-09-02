import { redirect } from 'next/navigation';

export default function UtrmcPostingsRedirect() {
  redirect('/dashboard/utrmc');
  return null;
}
