'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';
import authApi from '@/lib/api/auth';

export default function ResetPasswordConfirmPage() {
  const params = useParams();
  const uid = typeof params?.uid === 'string' ? params.uid : '';
  const token = typeof params?.token === 'string' ? params.token : '';

  const [formData, setFormData] = useState({
    newPassword: '',
    confirmPassword: '',
  });
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!uid || !token) {
      setError('Invalid or missing reset token.');
      return;
    }

    if (formData.newPassword.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    if (formData.newPassword !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      await authApi.passwordResetConfirm({
        uid,
        token,
        new_password: formData.newPassword,
        new_password2: formData.confirmPassword,
      });
      setSuccess(true);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const payload = err.response?.data as { error?: string; detail?: string; message?: string } | undefined;
        setError(payload?.error || payload?.detail || payload?.message || 'Failed to set password. Link may be expired.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-6 bg-white p-10 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#EAECEA] text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-[#2C3333]">
            Password Set Successfully
          </h2>
          <p className="text-sm text-[#7D8A8A]">
            Your password has been successfully configured. You can now access your account.
          </p>
          <div className="pt-2">
            <Link
              href="/login"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] shadow-sm transition-all duration-200"
            >
              Back to Sign In
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F2F4F3] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-6 bg-white p-10 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#EAECEA]">
        <div>
          <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-[#2C3333]">
            Set Your Password
          </h2>
          <p className="mt-3 text-center text-sm text-[#7D8A8A]">
            Configure a password to activate and secure your account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-[#FFF5F5] border border-[#FAD4D4] text-[#C53030] px-4 py-3 rounded-xl text-sm relative" data-testid="reset-error">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="newPassword" className="block text-sm font-medium text-[#4A5555] mb-1">
                New Password
              </label>
              <div className="relative">
                <input
                  id="newPassword"
                  name="newPassword"
                  type={showNewPassword ? 'text' : 'password'}
                  required
                  className="appearance-none block w-full px-4 py-3 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="Enter new password"
                  value={formData.newPassword}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                >
                  {showNewPassword ? 'Hide' : 'Show'}
                </button>
              </div>
              <p className="mt-1 text-xs text-gray-500">Must be at least 8 characters.</p>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-[#4A5555] mb-1">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  className="appearance-none block w-full px-4 py-3 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="Confirm new password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? 'Hide' : 'Show'}
                </button>
              </div>
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#859B9B] shadow-sm transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Set Password'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
