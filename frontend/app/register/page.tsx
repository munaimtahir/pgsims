'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';
import authApi from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPathForRole } from '@/lib/rbac';

export default function RegisterPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password2: '',
  });

  const [showPassword, setShowPassword] = useState(false);
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

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    if (formData.password !== formData.password2) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      const response = await authApi.register({
        username: formData.username.trim(),
        email: formData.email.trim(),
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        password: formData.password,
        password2: formData.password2,
        role: 'RESIDENT', // Public registration only supports role 'RESIDENT'
      });

      setSuccess(true);
      setAuth(response.user, response.tokens.access, response.tokens.refresh);

      // Redirect to role-specific dashboard
      router.push(getDashboardPathForRole(response.user.role));
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 403) {
          setError('Public registration is disabled. New accounts are provisioned by administrators only.');
        } else {
          const payload = err.response?.data as Record<string, unknown> | undefined;
          if (payload) {
            // Flatten errors if they are array fields
            const errMsgs = Object.entries(payload)
              .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
              .join('; ');
            setError(errMsgs || 'Registration failed. Please verify the input values.');
          } else {
            setError('Registration failed. Please try again.');
          }
        }
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
          <h2 className="text-3xl font-bold tracking-tight text-[#2C3333]">
            Registering...
          </h2>
          <p className="text-sm text-[#7D8A8A]">
            Setting up your portfolio and signing you in.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F2F4F3] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-6 bg-white p-10 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#EAECEA]">
        <div>
          <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-[#2C3333]">
            Create an Account
          </h2>
          <p className="mt-3 text-center text-sm text-[#7D8A8A]">
            Register to join SIMS and start tracking your training progress
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-[#FFF5F5] border border-[#FAD4D4] text-[#C53030] px-4 py-3 rounded-xl text-sm relative" data-testid="register-error">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-[#4A5555] mb-1">
                  First Name
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="John"
                  value={formData.first_name}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-[#4A5555] mb-1">
                  Last Name
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="Doe"
                  value={formData.last_name}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-[#4A5555] mb-1">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                placeholder="Enter unique username"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-[#4A5555] mb-1">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                placeholder="email@example.com"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-[#4A5555] mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="Enter password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
              <p className="mt-1 text-xs text-gray-500">Must be at least 8 characters.</p>
            </div>

            <div>
              <label htmlFor="password2" className="block text-sm font-medium text-[#4A5555] mb-1">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  id="password2"
                  name="password2"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                  placeholder="Confirm password"
                  value={formData.password2}
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
              {loading ? 'Creating account...' : 'Register'}
            </button>
          </div>

          <div className="text-center text-sm">
            <Link href="/login" className="font-medium text-[#647C7C] hover:text-[#4A5C5C] transition-colors">
              Already have an account? Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
