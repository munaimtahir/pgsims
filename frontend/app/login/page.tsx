'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPathForRole } from '@/lib/rbac';

export default function LoginPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError(''); // Clear error on input change
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.login(formData);
      setAuth(response.user, response.access, response.refresh);

      // Redirect to role-specific dashboard
      router.push(getDashboardPathForRole(response.user.role));
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string; error?: string } } };
      setError(
        error.response?.data?.detail ||
        error.response?.data?.error ||
        'Login failed. Please check your credentials.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F2F4F3] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-6 bg-white p-10 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#EAECEA]">
        <div>
          <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-[#2C3333]">
            Sign in to SIMS
          </h2>
          <p className="mt-3 text-center text-sm text-[#7D8A8A]">
            Postgraduate Student Information Management System
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-[#FFF5F5] border border-[#FAD4D4] text-[#C53030] px-4 py-3 rounded-xl text-sm relative">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-[#4A5555] mb-1">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="appearance-none block w-full px-4 py-3 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                placeholder="Enter your username"
                value={formData.username}
                onChange={handleChange}
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-[#4A5555] mb-1">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="appearance-none block w-full px-4 py-3 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="flex items-center justify-between mt-6">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-[#859B9B] focus:ring-[#859B9B] border-[#D5DBDB] rounded cursor-pointer"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-[#627070] cursor-pointer">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <Link href="/forgot-password" className="font-medium text-[#647C7C] hover:text-[#4A5C5C] transition-colors">
                Forgot password?
              </Link>
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#859B9B] shadow-sm transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center text-sm text-[#7D8A8A] mt-6">
            Registration is disabled. Contact your administrator for account creation.
          </div>
        </form>
      </div>
    </div>
  );
}
