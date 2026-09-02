import type { ReactNode } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import RoleDirectoryPage from './RoleDirectoryPage';
import { userbaseApi } from '@/lib/api/userbase';

jest.mock('@/components/auth/ProtectedRoute', () => ({
  __esModule: true,
  default: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ href, children }: { href: string; children: ReactNode }) => <a href={href}>{children}</a>,
}));

jest.mock('@/lib/api/userbase', () => ({
  userbaseApi: {
    users: { list: jest.fn() },
  },
}));

const mockedUserbaseApi = userbaseApi as unknown as {
  users: { list: jest.Mock };
};

describe('RoleDirectoryPage', () => {
  beforeEach(() => {
    mockedUserbaseApi.users.list.mockResolvedValue([
      { id: 1, username: 'jdoe', email: 'j@example.com', first_name: 'Jane', last_name: 'Doe', role: 'RESIDENT', is_active: true },
    ]);
  });

  it('loads the directory with the role filter on mount', async () => {
    render(<RoleDirectoryPage title="Residents" description="d" role="RESIDENT" />);
    await waitFor(() => expect(mockedUserbaseApi.users.list).toHaveBeenCalledWith({ role: 'RESIDENT' }));
    expect(await screen.findByText('Jane Doe')).toBeInTheDocument();
  });

  it('debounces the search box and includes it in the query', async () => {
    const user = userEvent.setup();
    render(<RoleDirectoryPage title="Residents" description="d" role="RESIDENT" />);
    await waitFor(() => expect(mockedUserbaseApi.users.list).toHaveBeenCalled());

    await user.type(screen.getByLabelText('Search directory'), 'jane');

    await waitFor(
      () => expect(mockedUserbaseApi.users.list).toHaveBeenLastCalledWith({ role: 'RESIDENT', search: 'jane' }),
      { timeout: 2000 }
    );
  });

  it('passes the active-status filter through to the API', async () => {
    const user = userEvent.setup();
    render(<RoleDirectoryPage title="Residents" description="d" role="RESIDENT" />);
    await waitFor(() => expect(mockedUserbaseApi.users.list).toHaveBeenCalled());

    await user.selectOptions(screen.getByLabelText('Filter by status'), 'inactive');

    await waitFor(() =>
      expect(mockedUserbaseApi.users.list).toHaveBeenLastCalledWith({ role: 'RESIDENT', active: false })
    );
  });

  it('shows "No records found" when the filtered result set is empty', async () => {
    mockedUserbaseApi.users.list.mockResolvedValue([]);
    render(<RoleDirectoryPage title="Residents" description="d" role="RESIDENT" />);
    expect(await screen.findByText('No records found.')).toBeInTheDocument();
  });
});
