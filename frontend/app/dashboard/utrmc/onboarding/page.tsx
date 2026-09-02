import { redirect } from 'next/navigation';

export default function UtrmcOnboardingRedirect() {
  redirect('/users/new');
  return null;
}
