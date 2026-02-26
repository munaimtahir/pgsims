'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-[#F2F4F3]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center max-w-4xl mx-auto bg-white p-12 rounded-[24px] shadow-[0_8px_30px_rgb(0,0,0,0.03)] border border-[#EAECEA]">
          <h1 className="text-5xl font-bold text-[#2C3333] sm:text-6xl md:text-6xl leading-tight">
            <span className="block mb-2">Postgraduate Student</span>
            <span className="block text-[#859B9B]">Information Management System</span>
          </h1>
          <p className="mt-8 max-w-2xl mx-auto text-base text-[#627070] sm:text-lg md:text-xl">
            A comprehensive, calm, and premium platform for managing postgraduate medical training,
            rotations, certificates, and academic records.
          </p>
          <div className="mt-10 max-w-md mx-auto sm:flex sm:justify-center gap-4">
            <div>
              <Link
                href="/login"
                className="w-full flex items-center justify-center px-8 py-3.5 border border-transparent text-base font-medium rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] shadow-sm transition-all duration-200 md:text-lg md:px-10"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
