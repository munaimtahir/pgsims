'use client';

import { useState } from 'react';
import axios from 'react';
import PageHeader from '@/components/ui/PageHeader';
import SectionCard from '@/components/ui/SectionCard';
import authApi from '@/lib/api/auth';

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.newPassword.length < 8) {
      setError('New password must be at least 8 characters long.');
      return;
    }

    if (formData.newPassword !== formData.confirmPassword) {
      setError('New passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      await authApi.changePassword({
        old_password: formData.oldPassword,
        new_password: formData.newPassword,
        new_password2: formData.confirmPassword,
      });
      setSuccess('Your password has been changed successfully.');
      setFormData({
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { error?: string; detail?: string; message?: string } } };
        const payload = axiosErr.response?.data;
        setError(payload?.error || payload?.detail || payload?.message || 'Failed to change password. Please verify current password.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pg-page">
      <PageHeader
        title="Change Password"
        description="Update your password to keep your account secure."
      />

      <div className="max-w-xl">
        <SectionCard title="Update Password">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-[#FFF5F5] border border-[#FAD4D4] text-[#C53030] px-4 py-3 rounded-xl text-sm relative" data-testid="change-error">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-xl text-sm relative" data-testid="change-success">
                {success}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="oldPassword" className="block text-sm font-medium text-[#4A5555] mb-1">
                  Current Password
                </label>
                <div className="relative">
                  <input
                    id="oldPassword"
                    name="oldPassword"
                    type={showOldPassword ? 'text' : 'password'}
                    required
                    className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
                    placeholder="Enter current password"
                    value={formData.oldPassword}
                    onChange={handleChange}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
                    onClick={() => setShowOldPassword(!showOldPassword)}
                  >
                    {showOldPassword ? 'Hide' : 'Show'}
                  </button>
                </div>
              </div>

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
                    className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
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
                  Confirm New Password
                </label>
                <div className="relative">
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    required
                    className="appearance-none block w-full px-4 py-2.5 border border-[#D5DBDB] bg-[#FAFBFA] text-[#2C3333] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#859B9B] focus:border-transparent sm:text-sm transition-colors duration-200"
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

            <div className="flex justify-end pt-2">
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2.5 border border-transparent text-sm font-medium rounded-xl text-white bg-[#859B9B] hover:bg-[#728787] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#859B9B] shadow-sm transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {loading ? 'Updating...' : 'Update Password'}
              </button>
            </div>
          </form>
        </SectionCard>
      </div>
    </div>
  );
}
