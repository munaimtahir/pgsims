import '@testing-library/jest-dom/jest-globals';
import { beforeEach, expect, it } from '@jest/globals';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import NewUserPage from './page';
import authApi from '@/lib/api/auth';
import { userbaseApi } from '@/lib/api/userbase';

const refresh = jest.fn();
jest.mock('next/navigation', () => ({ useRouter: () => ({ refresh }) }));
jest.mock('@/lib/api/auth', () => ({ __esModule: true, default: { getIdentityOptions: jest.fn() } }));
jest.mock('@/lib/api/userbase', () => ({ userbaseApi: { users: { list: jest.fn(), create: jest.fn() } } }));
const options = {
  hospitals: [{ id: 1, name: 'Hospital' }], departments: [{ id: 2, name: 'Department' }],
  programs: [{ id: 3, name: 'Program' }], academic_sessions: [{ id: 'session', name: 'Session' }],
  designations: [{ id: 'professor', name: 'Professor' }],
};
const change = (label: string, value: string) => fireEvent.change(screen.getByLabelText(label), { target: { value } });

beforeEach(() => {
  jest.clearAllMocks();
  window.history.replaceState({}, '', '/users/new');
  (authApi.getIdentityOptions as jest.Mock).mockResolvedValue(options);
  (userbaseApi.users.list as jest.Mock).mockResolvedValue([{ id: 4, username: 'sup004', full_name: 'Dr Supervisor' }, { id: 5, username: 'sup005' }]);
  (userbaseApi.users.create as jest.Mock).mockResolvedValue({ username: 'generated001' });
});

it.each(['ADMIN', 'RESIDENT', 'SUPERVISOR', 'SUPPORT_STAFF'])('creates %s with generated credentials and the selected role', async role => {
  window.history.replaceState({}, '', `/users/new?role=${role}`);
  render(<NewUserPage />);
  await waitFor(() => expect(screen.getByLabelText('Role')).toHaveValue(role));
  expect(Array.from((screen.getByLabelText('Role') as HTMLSelectElement).options).map(o => o.value)).toEqual(['ADMIN','RESIDENT','SUPERVISOR','SUPPORT_STAFF']);
  expect(screen.getByRole('button', { name: 'Create User' })).toBeDisabled();
  change('Full Name', '  Test   Person  ');
  fireEvent.click(screen.getByRole('button', { name: 'Create User' }));
  await screen.findByText('User created successfully');
  expect(userbaseApi.users.create).toHaveBeenCalledWith(expect.objectContaining({ role, username: undefined, password: undefined, first_name: 'Test', last_name: 'Person', is_active: true }));
  expect(screen.getByText('Temporary Password: pgfmu123')).toBeInTheDocument();
  expect(screen.getByLabelText('Full Name')).toHaveValue('');
  expect(refresh).toHaveBeenCalledTimes(1);
});

it('submits resident profile references, preserves custom credentials and supports copying/printing', async () => {
  const writeText = jest.fn().mockResolvedValue(undefined);
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
  const print = jest.spyOn(window, 'print').mockImplementation(() => undefined);
  render(<NewUserPage />);
  await screen.findByRole('option', { name: 'Dr Supervisor' });
  change('Full Name', 'Resident One'); change('Email', 'resident@example.invalid'); change('Phone', '12345');
  change('Username', ' custom001 '); change('Temporary Password', 'custom-password');
  change('Hospital / Training Site', '1'); change('Department', '2'); change('Training Program', '3');
  change('Academic Session', 'session'); change('Training Start Date', '2026-09-01'); change('Supervisor', '4');
  expect(screen.queryByLabelText('Unavailable Supervisor Name')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Create User' }));
  await screen.findByText('User created successfully');
  expect(userbaseApi.users.create).toHaveBeenCalledWith(expect.objectContaining({ username: 'custom001', password: 'custom-password', email: 'resident@example.invalid', phone_number: '12345', profile: expect.objectContaining({hospital: 1, department_ref: 2, program_ref: 3, academic_session_ref: 'session', supervisor_profile_id: 4, training_start_date: '2026-09-01'}) }));
  expect(screen.getByText('Temporary Password: custom-password')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Copy Credentials' }));
  expect(writeText).toHaveBeenCalledWith('generated001\ncustom-password');
  fireEvent.click(screen.getByRole('button', { name: 'Print Credentials' })); expect(print).toHaveBeenCalled();
  print.mockRestore();
});

it('accepts an unavailable supervisor and a single-part name', async () => {
  render(<NewUserPage />); await screen.findByRole('option', { name: 'Hospital' });
  change('Full Name', 'Resident'); change('Unavailable Supervisor Name', ' Dr Pending ');
  fireEvent.click(screen.getByRole('button', { name: 'Create User' })); await screen.findByText('User created successfully');
  expect(userbaseApi.users.create).toHaveBeenCalledWith(expect.objectContaining({ last_name: '', profile: expect.objectContaining({ supervisor_name: 'Dr Pending' }) }));
});

it('changes role to supervisor and submits its designation', async () => {
  render(<NewUserPage />); await screen.findByRole('option', { name: 'Hospital' });
  change('Role', 'SUPERVISOR'); change('Supervisor Designation', 'professor'); change('Full Name', 'Supervisor One');
  expect(screen.queryByLabelText('Training Program')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Create User' })); await screen.findByText('User created successfully');
  expect(userbaseApi.users.create).toHaveBeenCalledWith(expect.objectContaining({ role: 'SUPERVISOR', profile: expect.objectContaining({ designation_ref: 'professor' }) }));
});

it.each([{}, { response: undefined }, { response: { data: { full_name: ['Required'] } } }])('retains entered values and permits retry after failure %#', async error => {
  (userbaseApi.users.create as jest.Mock).mockRejectedValueOnce(error);
  render(<NewUserPage />); await screen.findByRole('option', { name: 'Hospital' });
  change('Full Name', 'Retry Person'); fireEvent.click(screen.getByRole('button', { name: 'Create User' }));
  await screen.findByText(error.response?.data ? JSON.stringify(error.response.data) : 'Unable to create user');
  expect(screen.getByLabelText('Full Name')).toHaveValue('Retry Person'); expect(refresh).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Create User' })); await screen.findByText('User created successfully');
});

it('falls back to resident for an invalid role and survives failed dropdown requests', async () => {
  window.history.replaceState({}, '', '/users/new?role=INVALID');
  (authApi.getIdentityOptions as jest.Mock).mockRejectedValue(new Error('offline'));
  (userbaseApi.users.list as jest.Mock).mockRejectedValue(new Error('offline'));
  render(<NewUserPage />); await screen.findByText('Failed to load master dropdown data');
  expect(screen.getByLabelText('Role')).toHaveValue('RESIDENT');
  change('Role', 'SUPERVISOR'); expect(screen.getByLabelText('Supervisor Designation')).toBeInTheDocument();
});

it('disables repeated submission while a create request is pending', async () => {
  let finish!: (value: { username: string }) => void;
  (userbaseApi.users.create as jest.Mock).mockReturnValue(new Promise(resolve => { finish = resolve; }));
  render(<NewUserPage />); await screen.findByRole('option', { name: 'Hospital' }); change('Full Name', 'Pending Person');
  fireEvent.click(screen.getByRole('button', { name: 'Create User' }));
  expect(screen.getByRole('button', { name: 'Creating...' })).toBeDisabled();
  finish({ username: 'created001' }); await screen.findByText('User created successfully');
  expect(userbaseApi.users.create).toHaveBeenCalledTimes(1);
});
