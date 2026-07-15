import { redirect } from 'next/navigation';

export default function UtrmcEligibilityRedirect() {
  redirect('/dashboard/utrmc');
  return null;
}
