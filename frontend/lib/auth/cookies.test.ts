import { syncAuthCookies, clearAuthCookies } from './cookies';

describe('auth cookies', () => {
  beforeEach(() => {
    // Clear cookies before each test
    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
  });

  describe('syncAuthCookies', () => {
    it('sets access token and role cookies', () => {
      // Mock JWT with exp: tomorrow
      const exp = Math.floor(Date.now() / 1000) + 3600;
      const payload = btoa(JSON.stringify({ exp }));
      const token = `header.${payload}.signature`;

      syncAuthCookies({ accessToken: token, role: 'resident' });

      expect(document.cookie).toContain('pgsims_access_token=header');
      expect(document.cookie).toContain('pgsims_user_role=resident');
      expect(document.cookie).toContain('pgsims_access_exp=');
    });

    it('clears cookies if params are null', () => {
      document.cookie = "pgsims_access_token=test";
      syncAuthCookies({ accessToken: null, role: null });
      expect(document.cookie).not.toContain('pgsims_access_token=test');
    });
  });

  describe('clearAuthCookies', () => {
    it('clears all auth cookies', () => {
      document.cookie = "pgsims_access_token=test";
      document.cookie = "pgsims_user_role=resident";
      
      clearAuthCookies();
      
      expect(document.cookie).not.toContain('pgsims_access_token');
      expect(document.cookie).not.toContain('pgsims_user_role');
    });
  });
});
