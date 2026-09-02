import { useAuthStore } from './authStore';

describe('authStore', () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      hasHydrated: true,
    });
    localStorage.clear();
  });

  it('initializes with default state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });

  it('sets auth data correctly', () => {
    const user = { id: 1, username: 'test', role: 'resident' } as any;
    const accessToken = 'access-token';
    const refreshToken = 'refresh-token';

    useAuthStore.getState().setAuth(user, accessToken, refreshToken);

    const state = useAuthStore.getState();
    expect(state.user).toEqual(user);
    expect(state.accessToken).toBe(accessToken);
    expect(state.isAuthenticated).toBe(true);
  });

  it('clears auth data on logout', () => {
    useAuthStore.setState({
      user: { id: 1, username: 'test', role: 'resident' } as any,
      isAuthenticated: true,
    });

    useAuthStore.getState().clearAuth();

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });
});
