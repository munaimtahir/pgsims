import { expect, test, type BrowserContext, type Page } from '@playwright/test';

type AuthPayload = {
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    full_name: string;
    role: string;
  };
  access: string;
  refresh: string;
};

const APP_BASE_URL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
const API_BASE_URL = process.env.E2E_API_URL ?? 'http://127.0.0.1:8014';

function parseExp(token: string): number {
  try {
    const [, payload] = token.split('.');
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
    const decoded = JSON.parse(Buffer.from(padded, 'base64').toString('utf-8')) as { exp?: number };
    return decoded.exp ?? Math.floor(Date.now() / 1000) + 3600;
  } catch {
    return Math.floor(Date.now() / 1000) + 3600;
  }
}

async function loginAsAdminWithSpoofedRole(
  context: BrowserContext,
  page: Page,
  spoofedRole: string
) {
  const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin123' }),
  });
  if (!response.ok) {
    throw new Error(`Admin login failed: ${response.status} ${await response.text()}`);
  }

  const payload = (await response.json()) as AuthPayload;
  const exp = parseExp(payload.access);
  const spoofedUser = { ...payload.user, role: spoofedRole };

  await context.clearCookies();
  await context.addCookies([
    { name: 'pgsims_access_token', value: payload.access, url: APP_BASE_URL },
    { name: 'pgsims_user_role', value: spoofedRole, url: APP_BASE_URL },
    { name: 'pgsims_access_exp', value: String(exp), url: APP_BASE_URL },
  ]);
  await page.addInitScript((authPayload) => {
    localStorage.setItem(
      'auth-storage',
      JSON.stringify({
        state: {
          user: authPayload.user,
          accessToken: authPayload.access,
          refreshToken: authPayload.refresh,
          isAuthenticated: true,
        },
        version: 0,
      })
    );
    localStorage.setItem('access_token', authPayload.access);
    localStorage.setItem('refresh_token', authPayload.refresh);
    localStorage.setItem('user', JSON.stringify(authPayload.user));
  }, { user: spoofedUser, access: payload.access, refresh: payload.refresh });
}

async function mockEmptyBaseline(page: Page, role: 'utrmc_admin' | 'supervisor' | 'pg') {
  await page.route('**/api/**', async (route) => {
    const { pathname, searchParams } = new URL(route.request().url());
    const respond = (body: unknown, status = 200) => route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify(body),
    });

    if (pathname === '/api/dashboard/utrmc/' || pathname === '/api/dashboard/utrmc') {
      return respond({
        cross_department_overview: {
          active_residents: 0,
          program_count: 0,
          pending_logbook_reviews: 0,
        },
        pending_synopsis_reviews: 0,
        pending_thesis_reviews: 0,
        pending_rotation_completion_verifications: 0,
        resident_milestone_readiness: [],
        readiness_summary: { fully_ready_count: 0, total_rows: 0 },
      });
    }

    if (pathname === '/api/hospitals/' || pathname === '/api/hospitals') {
      return respond([]);
    }
    if (pathname === '/api/departments/' || pathname === '/api/departments') {
      return respond([]);
    }
    if (pathname === '/api/users/' || pathname === '/api/users') {
      return respond([]);
    }
    if (pathname === '/api/hospital-departments/' || pathname === '/api/hospital-departments') {
      return respond([]);
    }
    if (pathname === '/api/resident-training/' || pathname === '/api/resident-training') {
      return respond([]);
    }
    if (pathname === '/api/rotations/' || pathname === '/api/rotations') {
      return respond([]);
    }
    if (pathname === '/api/submissions/synopsis/review-queue/' || pathname === '/api/submissions/synopsis/review-queue') {
      return respond({ count: 0, results: [] });
    }
    if (pathname === '/api/submissions/thesis/review-queue/' || pathname === '/api/submissions/thesis/review-queue') {
      return respond({ count: 0, results: [] });
    }
    if (pathname === '/api/rotation-completions/' || pathname === '/api/rotation-completions') {
      return respond({ count: 0, results: [] });
    }
    if (pathname === '/api/admin/data-quality/summary' || pathname === '/api/admin/data-quality/summary/') {
      return respond({
        total_users: 0,
        users_with_placeholder_email: 0,
        users_with_missing_dates: 0,
        complete_profiles: 0,
        incomplete_profiles: 0,
      });
    }
    if (pathname === '/api/admin/data-quality/users' || pathname === '/api/admin/data-quality/users/') {
      return respond([]);
    }
    if (pathname === '/api/admin/data-quality/audit' || pathname === '/api/admin/data-quality/audit/') {
      return respond([]);
    }

    if (role === 'supervisor') {
      if (pathname === '/api/supervisors/me/summary/' || pathname === '/api/supervisors/me/summary') {
        return respond({
          pending: { rotation_approvals: 0, leave_approvals: 0, research_approvals: 0 },
          residents: [],
        });
      }
      if (pathname === '/api/dashboard/supervisor/' || pathname === '/api/dashboard/supervisor') {
        return respond({
          pending: { rotation_approvals: 0, leave_approvals: 0, research_approvals: 0 },
          residents: [],
        });
      }
      if (pathname === '/api/utrmc/approvals/leaves/' || pathname === '/api/utrmc/approvals/leaves') {
        return respond([]);
      }
      if (pathname === '/api/supervisor/pending-leaves/' || pathname === '/api/supervisor/pending-leaves') {
        return respond([]);
      }
      if (pathname === '/api/logbook/review-queue/' || pathname === '/api/logbook/review-queue') {
        return respond({ count: 0, results: [] });
      }
      if (pathname === '/api/supervisor/operational-dashboard/' || pathname === '/api/supervisor/operational-dashboard') {
        return respond({
          assigned_residents: 0,
          pending_logbook_reviews: 0,
          returned_logbook_queue: 0,
          pending_rotation_applications: 0,
          pending_synopsis_reviews: 0,
          pending_thesis_reviews: 0,
          residents: [],
          lagging_residents: [],
          is_hod: false,
        });
      }
    }

    if (role === 'pg') {
      if (pathname === '/api/residents/me/summary/' || pathname === '/api/residents/me/summary') {
        return respond({
          training_record: null,
          rotation: { current: null, next: null },
          schedule: [],
          leaves: { active_count: 0, pending_count: 0, list: [] },
          postings: { active_count: 0, pending_count: 0 },
          research: { status: null, supervisor_name: null, synopsis_uploaded: false, university_submitted: false },
          thesis: { status: 'DRAFT', submitted_at: null },
          workshops: { total_completed: 0, required_for_imm: 0, required_for_final: 0, completed_list: [] },
          eligibility: {
            IMM: { status: null, reasons: [] },
            FINAL: { status: null, reasons: [] },
          },
        });
      }
      if (pathname === '/api/dashboard/resident/' || pathname === '/api/dashboard/resident') {
        return respond(null);
      }
      if (pathname === '/api/my/leaves/' || pathname === '/api/my/leaves') {
        return respond({ count: 0, results: [] });
      }
      if (pathname === '/api/my/rotations/' || pathname === '/api/my/rotations') {
        return respond({ count: 0, results: [] });
      }
    }

    return route.continue();
  });
}

test.describe('UI pilot readiness smoke', () => {
  test('UTRMC dashboard shows the operational summary and onboarding entry point', async ({ page, context }) => {
    await loginAsAdminWithSpoofedRole(context, page, 'utrmc_admin');
    await mockEmptyBaseline(page, 'utrmc_admin');

    await page.goto('/dashboard/utrmc');
    await expect(page.getByRole('heading', { name: 'UTRMC Dashboard' })).toBeVisible({ timeout: 15_000 });
    await expect(
      page.getByRole('main').getByRole('link', { name: /open onboarding tools/i }).first()
    ).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('main').getByText(/today’s attention/i).first()).toBeVisible({ timeout: 15_000 });
  });

  test('supervisor dashboard surfaces assigned work clearly', async ({ page, context }) => {
    await loginAsAdminWithSpoofedRole(context, page, 'supervisor');
    await mockEmptyBaseline(page, 'supervisor');

    await page.goto('/dashboard/supervisor');
    await expect(page.getByRole('heading', { name: 'Supervisor Dashboard' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('heading', { name: /my residents/i })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/No residents are assigned to you yet/i)).toBeVisible({ timeout: 15_000 });
  });

  test('resident dashboard shows a calm empty state when setup is missing', async ({ page, context }) => {
    await loginAsAdminWithSpoofedRole(context, page, 'pg');
    await mockEmptyBaseline(page, 'pg');

    await page.goto('/dashboard/resident');
    await expect(page.getByRole('heading', { name: 'My Training Dashboard' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/No active resident training record is linked yet/i)).toBeVisible({ timeout: 15_000 });
  });

  test('resident schedule shows a calm empty state when setup is missing', async ({ page, context }) => {
    await loginAsAdminWithSpoofedRole(context, page, 'pg');
    await mockEmptyBaseline(page, 'pg');

    await page.goto('/dashboard/resident/schedule');
    await expect(page.getByRole('heading', { name: 'My Schedule' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/No active resident training record is linked yet/i)).toBeVisible({ timeout: 15_000 });
  });

  test('data quality dashboard stays calm on an empty cleaned baseline', async ({ page, context }) => {
    await loginAsAdminWithSpoofedRole(context, page, 'utrmc_admin');
    await mockEmptyBaseline(page, 'utrmc_admin');

    await page.goto('/dashboard/utrmc/data-quality');
    await expect(page.getByRole('heading', { name: 'Data Quality Dashboard' })).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/Data quality checks are not available yet or no onboarding data has been added/i)).toBeVisible({
      timeout: 15_000,
    });
  });
});
