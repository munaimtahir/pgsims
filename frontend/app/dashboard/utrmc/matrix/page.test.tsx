import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import MatrixPage from './page';
import { userbaseApi } from '@/lib/api/userbase';
import { useAuthStore } from '@/store/authStore';

jest.mock('@/store/authStore', () => ({
  useAuthStore: jest.fn(),
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    hospitals: {
      list: jest.fn(),
    },
    departments: {
      list: jest.fn(),
    },
    matrix: {
      list: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
    },
  },
}));

const mockAuth = useAuthStore as unknown as jest.Mock;
const mockApi = userbaseApi as unknown as {
  hospitals: { list: jest.Mock };
  departments: { list: jest.Mock };
  matrix: { list: jest.Mock; create: jest.Mock; update: jest.Mock };
};

describe('UTRMC hospital-department matrix page', () => {
  beforeEach(() => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_admin' } });
    mockApi.hospitals.list.mockResolvedValue([{ id: 1, name: 'Teaching Hospital', code: 'TH', active: true }]);
    mockApi.departments.list.mockResolvedValue([{ id: 2, name: 'Medicine', code: 'MED', active: true }]);
    mockApi.matrix.list.mockResolvedValue([]);
    mockApi.matrix.create.mockResolvedValue({ id: 50, active: true });
    mockApi.matrix.update.mockResolvedValue({ id: 50, active: false });
  });

  it('lets UTRMC admin toggle an empty matrix cell into an active relationship', async () => {
    const user = userEvent.setup();
    render(<MatrixPage />);

    await waitFor(() => expect(screen.getByText('Teaching Hospital')).toBeInTheDocument());
    await user.click(screen.getByTitle('Inactive - click to activate'));

    await waitFor(() =>
      expect(mockApi.matrix.create).toHaveBeenCalledWith({
        hospital_id: 1,
        department_id: 2,
        active: true,
      })
    );
  });

  it('keeps matrix controls disabled for UTRMC read-only users', async () => {
    mockAuth.mockReturnValue({ user: { role: 'utrmc_user' } });
    mockApi.matrix.list.mockResolvedValue([
      {
        id: 50,
        hospital: { id: 1, name: 'Teaching Hospital', active: true },
        department: { id: 2, name: 'Medicine', code: 'MED', active: true },
        active: true,
      },
    ]);

    render(<MatrixPage />);

    await waitFor(() => expect(screen.getByText('Teaching Hospital')).toBeInTheDocument());
    const toggle = screen.getByTitle('Active (read-only)');

    expect(screen.getByText(/read-only/i)).toBeInTheDocument();
    expect(toggle).toBeDisabled();
  });
});
