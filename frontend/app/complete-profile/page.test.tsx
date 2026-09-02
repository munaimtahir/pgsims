import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useRouter } from 'next/navigation';
import CompleteProfilePage from './page';
import authApi, { AuthMeResponse, CompleteProfileForm, IdentityOptions, ResidentOnboardingState } from '@/lib/api/auth';

jest.mock('next/navigation', () => ({ useRouter: jest.fn() }));
jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    me: jest.fn(),
    getIdentityOptions: jest.fn(),
    getCompleteProfileForm: jest.fn(),
    completeProfile: jest.fn(),
    onboarding: jest.fn(),
    saveOnboardingField: jest.fn(),
    saveOnboardingDraft: jest.fn(),
    acceptResidentDeclaration: jest.fn(),
  },
}));

const push = jest.fn();
const emptyOptions: IdentityOptions = {
  institutions: [],
  training_sites: [],
  hospitals: [],
  departments: [],
  programs: [],
  academic_sessions: [],
  designations: [],
  specialties: [],
};

const residentState: ResidentOnboardingState = {
  profile_complete: false,
  onboarding_complete: false,
  required_onboarding_fields: ['full_name'],
  supervisor_status: 'NOT_STARTED',
  declaration_accepted: false,
  documents: [],
  workshops: [],
  baseline: {
    research: { title: '', topic_area: '', status: 'DRAFT' },
    thesis: { status: 'NOT_STARTED', notes: '' },
  },
  sections: [
    { key: 'identity', title: 'Identity', fields: [{ field: 'full_name', label: 'Full name', value: '', required: true }] },
    { key: 'enrollment', title: 'Enrollment', fields: [] },
    { key: 'supervisor', title: 'Supervisor linkage', fields: [] },
    { key: 'declaration', title: 'Declaration', fields: [] },
    { key: 'documents_baseline', title: 'Documents and academic baseline', fields: [] },
  ],
};

function me(role: AuthMeResponse['role'], allowedNextRoute = '/complete-profile'): AuthMeResponse {
  return {
    id: 1,
    username: 'user001',
    role,
    must_change_password: false,
    is_profile_complete: false,
    profile_type: `${role}Profile`,
    profile_id: 1,
    profile_status: 'INCOMPLETE',
    profile_schema_version: 1,
    completed_schema_version: 0,
    missing_required_fields: ['email'],
    allowed_next_route: allowedNextRoute,
  };
}

function form(profileType: string): CompleteProfileForm {
  return {
    profile_type: profileType,
    profile_status: 'INCOMPLETE',
    schema_version: 1,
    completed_schema_version: 0,
    missing_fields: [{ field: 'email', label: 'Email', source: 'user', input_type: 'email', required: true }],
  };
}

describe('CompleteProfilePage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({ push });
    (authApi.getIdentityOptions as jest.Mock).mockResolvedValue(emptyOptions);
    (authApi.onboarding as jest.Mock).mockResolvedValue(residentState);
    (authApi.saveOnboardingDraft as jest.Mock).mockResolvedValue(residentState);
  });

  ([
    ['ADMIN', 'AdminProfile'],
    ['SUPERVISOR', 'SupervisorProfile'],
    ['SUPPORT_STAFF', 'SupportStaffProfile'],
  ] as const).forEach(([role, profileType]) => {
    it(`renders the registry-driven form for ${role}`, async () => {
      (authApi.me as jest.Mock).mockResolvedValue(me(role));
      (authApi.getCompleteProfileForm as jest.Mock).mockResolvedValue(form(profileType));

      render(<CompleteProfilePage />);

      expect(await screen.findByRole('heading', { name: 'Complete Profile' })).toBeInTheDocument();
      expect(screen.getByLabelText('Email')).toBeInTheDocument();
      expect(authApi.onboarding).not.toHaveBeenCalled();
    });
  });

  it('submits a non-resident profile and follows the backend route', async () => {
    (authApi.me as jest.Mock).mockResolvedValue(me('ADMIN'));
    (authApi.getCompleteProfileForm as jest.Mock).mockResolvedValue(form('AdminProfile'));
    (authApi.completeProfile as jest.Mock).mockResolvedValue({ ...me('ADMIN', '/dashboard/utrmc'), is_profile_complete: true });
    const user = userEvent.setup();

    render(<CompleteProfilePage />);
    await user.type(await screen.findByLabelText('Email'), 'admin@example.com');
    await user.click(screen.getByRole('button', { name: 'Save Profile' }));

    await waitFor(() => expect(authApi.completeProfile).toHaveBeenCalledWith({ email: 'admin@example.com' }));
    expect(push).toHaveBeenCalledWith('/dashboard/utrmc');
  });

  it('renders resident onboarding only for residents', async () => {
    (authApi.me as jest.Mock).mockResolvedValue(me('RESIDENT'));

    render(<CompleteProfilePage />);

    expect(await screen.findByRole('heading', { name: 'Resident onboarding' })).toBeInTheDocument();
    expect(screen.getByLabelText(/^Full name/)).toBeInTheDocument();
    expect(authApi.getCompleteProfileForm).not.toHaveBeenCalled();
  });

  it('does not advance when a resident draft save fails', async () => {
    (authApi.me as jest.Mock).mockResolvedValue(me('RESIDENT'));
    (authApi.saveOnboardingDraft as jest.Mock).mockRejectedValue(new Error('offline'));
    const user = userEvent.setup();

    render(<CompleteProfilePage />);
    await screen.findByRole('heading', { name: 'Resident onboarding' });
    await user.click(screen.getByRole('button', { name: 'Continue' }));

    expect(await screen.findByText('Draft could not be saved. Please retry.')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Identity' })).toBeInTheDocument();
    expect(push).not.toHaveBeenCalled();
  });

  it('keeps the resident on the page when backend completion is still required', async () => {
    (authApi.me as jest.Mock)
      .mockResolvedValueOnce(me('RESIDENT'))
      .mockResolvedValueOnce(me('RESIDENT', '/complete-profile'));
    const user = userEvent.setup();

    render(<CompleteProfilePage />);
    await screen.findByRole('heading', { name: 'Resident onboarding' });
    await user.click(screen.getByRole('button', { name: /5\. Documents and academic baseline/ }));
    await user.click(screen.getByRole('button', { name: 'Finish onboarding' }));

    expect(await screen.findByText('Complete all required fields and accept the declaration before continuing.')).toBeInTheDocument();
    expect(push).not.toHaveBeenCalled();
  });
});
