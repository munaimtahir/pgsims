import { redirect } from 'next/navigation';

export default function ResidentThesisRedirect() {
  redirect('/dashboard/resident');
  return null;
}
