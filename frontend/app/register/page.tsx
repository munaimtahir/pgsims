import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F2F4F3] px-4">
      <div className="max-w-md w-full bg-white p-10 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#EAECEA] text-center">
        <h1 className="text-2xl font-bold text-[#2C3333]">Registration is disabled</h1>
        <p className="mt-3 text-sm text-[#7D8A8A]">
          New accounts are provisioned by administrators only.
        </p>
        <Link
          href="/login"
          className="mt-6 inline-flex items-center justify-center px-6 py-3 rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] transition-colors"
        >
          Back to login
        </Link>
      </div>
    </div>
  );
}
