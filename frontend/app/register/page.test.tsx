import { render, screen } from '@testing-library/react';
import RegisterPage from './page';
import authApi from '@/lib/api/auth';

jest.mock('@/lib/api/auth', () => ({
  __esModule: true,
  default: {
    register: jest.fn(),
  },
}));

jest.mock('@/store/authStore', () => ({
  useAuthStore: () => ({
    setAuth: jest.fn(),
  }),
}));

const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

const mockedRegister = authApi.register as jest.MockedFunction<typeof authApi.register>;

describe('RegisterPage', () => {
  beforeEach(() => {
    mockedRegister.mockReset();
    mockPush.mockReset();
  });

  it('explains that public registration is disabled', () => {
    render(<RegisterPage />);
    expect(screen.getByRole('heading', { name: /registration is disabled/i })).toBeInTheDocument();
    expect(screen.getByText(/new accounts are provisioned by administrators only/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /back to login/i })).toHaveAttribute('href', '/login');
    expect(mockedRegister).not.toHaveBeenCalled();
  });

});
