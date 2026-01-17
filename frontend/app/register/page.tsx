'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authApi, type RegisterData } from '@/lib/api/auth';
import { useAuthStore } from '@/store/authStore';
import apiClient from '@/lib/api/client';

interface Supervisor {
  id: number;
  name: string;
}

export default function RegisterPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    role: 'pg' as 'pg' | 'supervisor' | 'admin',
    specialty: '',
    year: '',
    supervisor: undefined as number | undefined,
    phone_number: '',
  });
  const [supervisors, setSupervisors] = useState<Supervisor[]>([]);
  const [loadingSupervisors, setLoadingSupervisors] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch supervisors when specialty changes and role is 'pg'
  useEffect(() => {
    const fetchSupervisors = async () => {
      if (formData.role === 'pg' && formData.specialty) {
        setLoadingSupervisors(true);
        try {
          // Try the API endpoint for supervisors by specialty
          // Note: This endpoint may need to be exposed via /api/ route
          // For now, we'll try both patterns
          let response;
          try {
            response = await apiClient.get<{ supervisors: Supervisor[] }>(
              `/users/api/supervisors/specialty/${formData.specialty}/`
            );
          } catch {
            // If that fails, try without auth (since registration is public)
            response = await apiClient.get<{ supervisors: Supervisor[] }>(
              `/users/api/supervisors/specialty/${formData.specialty}/`,
              { headers: {} }
            );
          }
          setSupervisors(response.data.supervisors || []);
        } catch (err) {
          console.error('Failed to fetch supervisors:', err);
          setSupervisors([]);
        } finally {
          setLoadingSupervisors(false);
        }
      } else {
        setSupervisors([]);
        setFormData(prev => ({ ...prev, supervisor: undefined }));
      }
    };

    fetchSupervisors();
  }, [formData.specialty, formData.role]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (formData.password !== formData.password2) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    // Build registration payload (remove password2, ensure required fields)
    const payload: Record<string, unknown> = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      password2: formData.password2,
      first_name: formData.first_name,
      last_name: formData.last_name,
      role: formData.role,
    };

    if (formData.specialty) {
      payload.specialty = formData.specialty;
    }
    if (formData.year) {
      payload.year = formData.year;
    }
    if (formData.supervisor) {
      payload.supervisor = String(formData.supervisor);
    }
    if (formData.phone_number) {
      payload.phone_number = formData.phone_number;
    }

    try {
      const response = await authApi.register(payload as unknown as RegisterData);
      setAuth(response.user, response.tokens.access, response.tokens.refresh);
      
      // Redirect to role-specific dashboard
      const role = response.user.role;
      if (role === 'admin') {
        router.push('/dashboard/admin');
      } else if (role === 'supervisor') {
        router.push('/dashboard/supervisor');
      } else if (role === 'pg') {
        router.push('/dashboard/pg');
      } else {
        router.push('/dashboard');
      }
    } catch (err: unknown) {
      const error = err as { response?: { data?: Record<string, unknown> } };
      const errors = error.response?.data;
      if (typeof errors === 'object' && errors !== null) {
        // Display first error
        const firstError = Object.values(errors)[0];
        setError(Array.isArray(firstError) ? firstError[0] : String(firstError));
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create Account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Register for SIMS
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                  First Name *
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.first_name}
                  onChange={handleChange}
                />
              </div>
              
              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                  Last Name *
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.last_name}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Username *
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email *
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                Role *
              </label>
              <select
                id="role"
                name="role"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                value={formData.role}
                onChange={handleChange}
              >
                <option value="pg">Postgraduate Student</option>
                <option value="supervisor">Supervisor</option>
                <option value="admin">Administrator</option>
              </select>
            </div>

            {formData.role === 'pg' && (
              <>
                <div>
                  <label htmlFor="specialty" className="block text-sm font-medium text-gray-700">
                    Specialty *
                  </label>
                  <select
                    id="specialty"
                    name="specialty"
                    required
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    value={formData.specialty}
                    onChange={handleChange}
                  >
                    <option value="">Select Specialty</option>
                    <option value="urology">Urology</option>
                    <option value="medicine">Medicine</option>
                    <option value="surgery">Surgery</option>
                    <option value="cardiology">Cardiology</option>
                    <option value="neurology">Neurology</option>
                    <option value="pediatrics">Pediatrics</option>
                    <option value="orthopedics">Orthopedics</option>
                    <option value="anesthesiology">Anesthesiology</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="year" className="block text-sm font-medium text-gray-700">
                    Year *
                  </label>
                  <input
                    id="year"
                    name="year"
                    type="text"
                    required
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="e.g., 2024, Year 1"
                    value={formData.year}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label htmlFor="supervisor" className="block text-sm font-medium text-gray-700">
                    Supervisor *
                  </label>
                  {loadingSupervisors ? (
                    <div className="mt-1 text-sm text-gray-500">Loading supervisors...</div>
                  ) : supervisors.length > 0 ? (
                    <select
                      id="supervisor"
                      name="supervisor"
                      required
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      value={formData.supervisor || ''}
                      onChange={(e) => setFormData({ ...formData, supervisor: e.target.value ? parseInt(e.target.value) : undefined })}
                    >
                      <option value="">Select Supervisor</option>
                      {supervisors.map((sup) => (
                        <option key={sup.id} value={sup.id}>
                          {sup.name}
                        </option>
                      ))}
                    </select>
                  ) : formData.specialty ? (
                    <div className="mt-1 text-sm text-red-600">
                      No supervisors available for this specialty. Please select a different specialty.
                    </div>
                  ) : (
                    <div className="mt-1 text-sm text-gray-500">
                      Please select a specialty first.
                    </div>
                  )}
                </div>
              </>
            )}

            {formData.role === 'supervisor' && (
              <div>
                <label htmlFor="specialty" className="block text-sm font-medium text-gray-700">
                  Specialty *
                </label>
                <select
                  id="specialty"
                  name="specialty"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.specialty}
                  onChange={handleChange}
                >
                  <option value="">Select Specialty</option>
                  <option value="urology">Urology</option>
                  <option value="medicine">Medicine</option>
                  <option value="surgery">Surgery</option>
                  <option value="cardiology">Cardiology</option>
                  <option value="neurology">Neurology</option>
                  <option value="pediatrics">Pediatrics</option>
                  <option value="orthopedics">Orthopedics</option>
                  <option value="anesthesiology">Anesthesiology</option>
                </select>
              </div>
            )}

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password *
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="password2" className="block text-sm font-medium text-gray-700">
                Confirm Password *
              </label>
              <input
                id="password2"
                name="password2"
                type="password"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                value={formData.password2}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400"
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </div>

          <div className="text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign in here
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
