/**
 * PGSIMS Screenshot Tour
 *
 * Captures every screen in the application:
 *   - Public / auth pages
 *   - Every role dashboard and sub-page
 *   - Every workflow step (modals, forms, interactions)
 *
 * Output grouped into: OUT/screenshots/<group>/<name>.png
 *
 * Groups:
 *   01-public        — login, register, forgot-password, unauthorized
 *   02-utrmc-admin   — all UTRMC management pages + modals
 *   03-supervisor    — supervisor overview + sub-pages
 *   04-resident      — resident (pg) all pages
 *   05-workflow-hospital-crud     — create hospital step by step
 *   06-workflow-dept-crud         — create department step by step
 *   07-workflow-user-management   — user management steps
 *   08-workflow-supervision       — supervision link steps
 *   09-workflow-supervisor-review — supervisor research approvals flow
 *   10-workflow-resident-training — resident training workflow steps
 */

import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';
import * as path from 'path';

// ─── helper ──────────────────────────────────────────────────────────────────

const BASE = process.env.E2E_SCREENSHOTS_DIR ?? 'pw-screenshots';

function ss(group: string, name: string): string {
  return path.join(BASE, group, `${name}.png`);
}

async function shot(page: any, group: string, name: string) {
  // Wait for animations / transitions to settle
  await page.waitForTimeout(600);
  await page.screenshot({
    path: ss(group, name),
    fullPage: true,
  });
}

// ─── PUBLIC / AUTH PAGES ─────────────────────────────────────────────────────

test.describe('01 — Public & Auth pages', () => {
  test('login page', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    await shot(page, '01-public', '01-login-page');
  });

  test('login page — form validation (empty submit)', async ({ page }) => {
    await page.goto('/login');
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForTimeout(400);
    await shot(page, '01-public', '02-login-empty-validation');
  });

  test('login page — invalid credentials error', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username/i).fill('invalid_user');
    await page.getByLabel(/password/i).fill('WrongPass!');
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForTimeout(2000);
    await shot(page, '01-public', '03-login-invalid-credentials-error');
  });

  test('register page', async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('networkidle');
    await shot(page, '01-public', '04-register-page');
  });

  test('unauthorized page', async ({ page }) => {
    await page.goto('/unauthorized');
    await page.waitForLoadState('networkidle');
    await shot(page, '01-public', '05-unauthorized-page');
  });

  test('forgot password page', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.waitForLoadState('networkidle');
    await shot(page, '01-public', '06-forgot-password-page');
  });

  test('home page root', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await shot(page, '01-public', '07-home-root');
  });
});

// ─── UTRMC ADMIN DASHBOARD ───────────────────────────────────────────────────

test.describe('02 — UTRMC Admin dashboard', () => {
  test('01 overview / home', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '01-overview');
  });

  test('02 hospitals list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '02-hospitals-list');
  });

  test('03 departments list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/departments');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '03-departments-list');
  });

  test('04 department roster (Surgery dept)', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    // First find Surgery department id
    const appBase = process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk';
    const token = await (async () => {
      await page.goto('/dashboard/utrmc');
      return page.evaluate(() => {
        const raw = localStorage.getItem('auth-storage');
        if (!raw) return '';
        const p = JSON.parse(raw) as { state?: { accessToken?: string } };
        return p.state?.accessToken ?? '';
      });
    })();
    const resp = await page.request.get(`${appBase}/api/departments/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (resp.ok()) {
      const data = await resp.json() as any;
      const depts = Array.isArray(data) ? data : data.results ?? [];
      const surgery = depts.find((d: any) => /surg/i.test(d.name));
      if (surgery) {
        await page.goto(`/dashboard/utrmc/departments/${surgery.id}/roster`);
        await page.waitForLoadState('networkidle');
        await shot(page, '02-utrmc-admin', '04-department-roster');
      }
    }
  });

  test('05 users list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '05-users-list');
  });

  test('06 supervision links', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '06-supervision-links');
  });

  test('07 hospital-department matrix', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/matrix');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '07-hd-matrix');
  });

  test('08 programs', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/programs');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '08-programs');
  });

  test('09 eligibility monitoring', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/eligibility-monitoring');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '09-eligibility-monitoring');
  });

  test('10 HOD page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/hod');
    await page.waitForLoadState('networkidle');
    await shot(page, '02-utrmc-admin', '10-hod-page');
  });

  test('11 sidebar — collapsed state', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    // Collapse sidebar
    const collapseBtn = page.locator('[data-testid="sidebar-collapse-btn"], button[aria-label*="collapse"], button[aria-label*="sidebar"]').first();
    const hasColl = await collapseBtn.isVisible().catch(() => false);
    if (hasColl) {
      await collapseBtn.click();
      await page.waitForTimeout(500);
    }
    await shot(page, '02-utrmc-admin', '11-sidebar-collapsed');
  });
});

// ─── UTRMC ADMIN — LOGGED IN AS UTRMC_USER ───────────────────────────────────

test.describe('02b — UTRMC User (read-only) dashboard', () => {
  test('01 utrmc_user overview', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    await shot(page, '02b-utrmc-user', '01-overview');
  });

  test('02 utrmc_user hospitals', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.waitForLoadState('networkidle');
    await shot(page, '02b-utrmc-user', '02-hospitals');
  });

  test('03 utrmc_user departments', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_user');
    await page.goto('/dashboard/utrmc/departments');
    await page.waitForLoadState('networkidle');
    await shot(page, '02b-utrmc-user', '03-departments');
  });
});

// ─── SUPERVISOR DASHBOARD ─────────────────────────────────────────────────────

test.describe('03 — Supervisor dashboard', () => {
  test('01 overview', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await page.waitForLoadState('networkidle');
    await shot(page, '03-supervisor', '01-overview');
  });

  test('02 research approvals — list', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/research-approvals');
    await page.waitForLoadState('networkidle');
    await shot(page, '03-supervisor', '02-research-approvals-list');
  });

  test('03 resident progress view (e2e_pg)', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    // Find e2e_pg's id
    const appBase = process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk';
    await page.goto('/dashboard/supervisor');
    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const p = JSON.parse(raw) as { state?: { accessToken?: string } };
      return p.state?.accessToken ?? '';
    });
    const resp = await page.request.get(`${appBase}/api/supervisors/me/residents/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (resp.ok()) {
      const data = await resp.json() as any;
      const residents = Array.isArray(data) ? data : data.results ?? [];
      const pg = residents.find((r: any) => r.username === 'e2e_pg' || r.full_name?.includes('E2E'));
      if (pg) {
        await page.goto(`/dashboard/supervisor/residents/${pg.id}/progress`);
        await page.waitForLoadState('networkidle');
        await shot(page, '03-supervisor', '03-resident-progress-detail');
      } else {
        // Take screenshot of residents list anyway
        await shot(page, '03-supervisor', '03-residents-list-no-id');
      }
    } else {
      await shot(page, '03-supervisor', '03-residents-api-not-available');
    }
  });

  test('04 supervisor — sidebar detail', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await page.waitForLoadState('networkidle');
    // Hover sidebar to show tooltips / full labels
    await page.locator('nav, aside').first().hover().catch(() => {});
    await page.waitForTimeout(400);
    await shot(page, '03-supervisor', '04-sidebar-detail');
  });
});

// ─── RESIDENT (PG) DASHBOARD ─────────────────────────────────────────────────

test.describe('04 — Resident (PG) dashboard', () => {
  test('01 main dashboard', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '01-main-dashboard');
  });

  test('02 schedule / rotations', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '02-schedule-rotations');
  });

  test('03 academic progress', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/progress');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '03-academic-progress');
  });

  test('04 research — wizard step 1 (default)', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/research');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '04-research-wizard-step1');
  });

  test('05 thesis', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/thesis');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '05-thesis-page');
  });

  test('06 workshops', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/workshops');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '06-workshops-page');
  });

  test('07 PG redirect page (legacy /dashboard/pg)', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/pg');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '07-pg-legacy-redirect');
  });

  test('08 resident sidebar — full nav', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await page.waitForLoadState('networkidle');
    await shot(page, '04-resident', '08-sidebar-full-nav');
  });
});

// ─── WORKFLOW: HOSPITAL CREATE ────────────────────────────────────────────────

test.describe('05 — Workflow: Create Hospital', () => {
  test('step 1 — hospitals list (before)', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.waitForLoadState('networkidle');
    await shot(page, '05-workflow-hospital-crud', '01-hospitals-list-before');
  });

  test('step 2 — Add Hospital modal opens', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.getByRole('button', { name: /add hospital/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).toBeVisible();
    await shot(page, '05-workflow-hospital-crud', '02-add-hospital-modal-empty');
  });

  test('step 3 — form filled in', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.getByRole('button', { name: /add hospital/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    await boxes[0].fill('Al-Shifa Teaching Hospital');
    if (boxes.length > 1) await boxes[1].fill('ASTH');
    await shot(page, '05-workflow-hospital-crud', '03-add-hospital-form-filled');
  });

  test('step 4 — saved (modal closed, list updated)', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.getByRole('button', { name: /add hospital/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    const suffix = `SS-${Date.now().toString().slice(-5)}`;
    await boxes[0].fill(`Screenshot Hospital ${suffix}`);
    if (boxes.length > 1) await boxes[1].fill(`SH${Date.now().toString().slice(-5)}`);
    await Promise.all([
      page.waitForResponse(r => r.url().includes('/api/hospitals/') && r.request().method() === 'POST', { timeout: 15000 }),
      modal.getByRole('button', { name: 'Save' }).click(),
    ]);
    await page.waitForTimeout(1000);
    await shot(page, '05-workflow-hospital-crud', '04-after-save-list-refreshed');
  });

  test('step 5 — Cancel discards (modal closes without saving)', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/hospitals');
    await page.getByRole('button', { name: /add hospital/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    await boxes[0].fill('Hospital to be cancelled');
    await shot(page, '05-workflow-hospital-crud', '05-cancel-before-click');
    await modal.getByRole('button', { name: /cancel/i }).click();
    await expect(page.getByRole('heading', { name: /add hospital/i })).not.toBeVisible({ timeout: 5000 });
    await shot(page, '05-workflow-hospital-crud', '06-after-cancel-modal-closed');
  });
});

// ─── WORKFLOW: DEPARTMENT CREATE ──────────────────────────────────────────────

test.describe('06 — Workflow: Create Department', () => {
  test('step 1 — departments list', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');
    await page.waitForLoadState('networkidle');
    await shot(page, '06-workflow-dept-crud', '01-departments-list');
  });

  test('step 2 — Add Department modal open', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');
    await page.getByRole('button', { name: /add department/i }).click();
    await expect(page.getByRole('heading', { name: /add department/i })).toBeVisible();
    await shot(page, '06-workflow-dept-crud', '02-add-department-modal-empty');
  });

  test('step 3 — form filled', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');
    await page.getByRole('button', { name: /add department/i }).click();
    await expect(page.getByRole('heading', { name: /add department/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    await boxes[0].fill('Cardiology');
    if (boxes.length > 1) await boxes[1].fill('CARD');
    await shot(page, '06-workflow-dept-crud', '03-form-filled');
  });

  test('step 4 — saved successfully', async ({ page, context }) => {
    await loginAs(context, page, 'admin');
    await page.goto('/dashboard/utrmc/departments');
    await page.getByRole('button', { name: /add department/i }).click();
    await expect(page.getByRole('heading', { name: /add department/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    const suffix = `SS-${Date.now().toString().slice(-5)}`;
    await boxes[0].fill(`Screenshot Dept ${suffix}`);
    if (boxes.length > 1) await boxes[1].fill(`SD${Date.now().toString().slice(-5)}`);
    await Promise.all([
      page.waitForResponse(r => r.url().includes('/api/departments/') && r.request().method() === 'POST', { timeout: 15000 }),
      modal.getByRole('button', { name: 'Save' }).click(),
    ]);
    await page.waitForTimeout(1000);
    await shot(page, '06-workflow-dept-crud', '04-after-save');
  });
});

// ─── WORKFLOW: USER MANAGEMENT ────────────────────────────────────────────────

test.describe('07 — Workflow: User Management', () => {
  test('step 1 — users list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.waitForLoadState('networkidle');
    await shot(page, '07-workflow-user-management', '01-users-list');
  });

  test('step 2 — Add User modal open', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.getByRole('button', { name: /add user/i }).click();
    await expect(page.getByRole('heading', { name: /add user/i })).toBeVisible();
    await shot(page, '07-workflow-user-management', '02-add-user-modal-empty');
  });

  test('step 3 — Add User form filled', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.getByRole('button', { name: /add user/i }).click();
    await expect(page.getByRole('heading', { name: /add user/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    const boxes = await modal.getByRole('textbox').all();
    if (boxes[0]) await boxes[0].fill('dr_screenshot');
    if (boxes[1]) await boxes[1].fill('dr.screenshot@utrmc.pk');
    if (boxes[2]) await boxes[2].fill('SecurePass123!');
    await shot(page, '07-workflow-user-management', '03-add-user-form-filled');
  });

  test('step 4 — Add User validation (empty submit)', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.getByRole('button', { name: /add user/i }).click();
    await expect(page.getByRole('heading', { name: /add user/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    await modal.getByRole('button', { name: 'Save' }).click();
    await page.waitForTimeout(800);
    await shot(page, '07-workflow-user-management', '04-add-user-validation-error');
  });

  test('step 5 — role dropdown visible', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/users');
    await page.getByRole('button', { name: /add user/i }).click();
    await expect(page.getByRole('heading', { name: /add user/i })).toBeVisible();
    const modal = page.locator('.fixed.inset-0').last();
    // Open role selector
    const select = modal.locator('select').first();
    const hasSelect = await select.isVisible().catch(() => false);
    if (hasSelect) await select.click();
    await page.waitForTimeout(400);
    await shot(page, '07-workflow-user-management', '05-role-dropdown-open');
  });
});

// ─── WORKFLOW: SUPERVISION LINKS ──────────────────────────────────────────────

test.describe('08 — Workflow: Supervision Links', () => {
  test('step 1 — supervision page', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');
    await page.waitForLoadState('networkidle');
    await shot(page, '08-workflow-supervision', '01-supervision-list');
  });

  test('step 2 — Add Supervision Link modal', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/supervision');
    await page.waitForLoadState('networkidle');
    const addBtn = page.getByRole('button', { name: /add|create|link/i }).first();
    const hasBtn = await addBtn.isVisible().catch(() => false);
    if (hasBtn) {
      await addBtn.click();
      await page.waitForTimeout(600);
      await shot(page, '08-workflow-supervision', '02-add-supervision-modal-open');
      const cancelBtn = page.getByRole('button', { name: /cancel/i });
      if (await cancelBtn.isVisible().catch(() => false)) await cancelBtn.click();
    } else {
      await shot(page, '08-workflow-supervision', '02-supervision-no-add-button');
    }
  });
});

// ─── WORKFLOW: SUPERVISOR RESEARCH APPROVAL ───────────────────────────────────

test.describe('09 — Workflow: Supervisor Research Review', () => {
  test('step 1 — research approvals queue (empty/pending)', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/research-approvals');
    await page.waitForLoadState('networkidle');
    await shot(page, '09-workflow-supervisor-review', '01-research-approvals-queue');
  });

  test('step 2 — supervisor dashboard resident cards', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    await page.waitForLoadState('networkidle');
    await shot(page, '09-workflow-supervisor-review', '02-supervisor-dashboard-residents');
  });

  test('step 3 — supervisor API summary state', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');
    const appBase = process.env.E2E_BASE_URL ?? 'https://pgsims.alshifalab.pk';
    const token = await page.evaluate(() => {
      const raw = localStorage.getItem('auth-storage');
      if (!raw) return '';
      const p = JSON.parse(raw) as { state?: { accessToken?: string } };
      return p.state?.accessToken ?? '';
    });
    // Show the API state visually via the rendered dashboard
    await page.waitForTimeout(1500);
    await shot(page, '09-workflow-supervisor-review', '03-supervisor-dashboard-loaded');
  });
});

// ─── WORKFLOW: RESIDENT TRAINING ──────────────────────────────────────────────

test.describe('10 — Workflow: Resident Training Journey', () => {
  test('step 1 — resident dashboard home', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '01-resident-home-dashboard');
  });

  test('step 2 — schedule (rotation calendar)', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '02-rotation-schedule');
  });

  test('step 3 — academic progress tracker', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/progress');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '03-academic-progress-tracker');
  });

  test('step 4 — research wizard — step 1 (Topic & Supervisor)', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/research');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '04-research-wizard-step1-topic');
  });

  test('step 5 — research wizard — step 2 (Upload Synopsis) — click next', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/research');
    await page.waitForLoadState('networkidle');
    // Try to advance to step 2
    const nextBtn = page.getByRole('button', { name: /next|upload synopsis|step 2/i }).first();
    const hasNext = await nextBtn.isVisible().catch(() => false);
    if (hasNext) {
      await nextBtn.click();
      await page.waitForTimeout(600);
    }
    await shot(page, '10-workflow-resident-training', '05-research-wizard-step2-synopsis');
  });

  test('step 6 — thesis management page', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/thesis');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '06-thesis-page');
  });

  test('step 7 — workshops list', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/workshops');
    await page.waitForLoadState('networkidle');
    await shot(page, '10-workflow-resident-training', '07-workshops-list');
  });
});

// ─── RBAC VISUAL: WRONG ROLE ACCESS ──────────────────────────────────────────

test.describe('11 — RBAC: Wrong role redirect screens', () => {
  test('pg tries to access UTRMC → redirect', async ({ page, context }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    await shot(page, '11-rbac-redirects', '01-pg-tries-utrmc-redirect');
  });

  test('supervisor tries to access UTRMC → redirect', async ({ page, context }) => {
    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    await shot(page, '11-rbac-redirects', '02-supervisor-tries-utrmc-redirect');
  });

  test('utrmc_admin tries to access supervisor → redirect', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/supervisor');
    await page.waitForLoadState('networkidle');
    await shot(page, '11-rbac-redirects', '03-utrmc-tries-supervisor-redirect');
  });

  test('unauthenticated access → login page', async ({ page }) => {
    await page.goto('/dashboard/utrmc');
    await page.waitForLoadState('networkidle');
    await shot(page, '11-rbac-redirects', '04-unauthenticated-redirected-to-login');
  });
});

// ─── H-D MATRIX WORKFLOW ─────────────────────────────────────────────────────

test.describe('12 — Workflow: Hospital-Department Matrix', () => {
  test('step 1 — matrix overview', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/matrix');
    await page.waitForLoadState('networkidle');
    await shot(page, '12-workflow-hd-matrix', '01-matrix-overview');
  });

  test('step 2 — matrix with UTRMC hospital expanded', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/matrix');
    await page.waitForLoadState('networkidle');
    // Try to expand/interact with first hospital row
    const firstRow = page.locator('table tr, [role="row"]').nth(1);
    const hasRow = await firstRow.isVisible().catch(() => false);
    if (hasRow) {
      await firstRow.click().catch(() => {});
      await page.waitForTimeout(600);
    }
    await shot(page, '12-workflow-hd-matrix', '02-matrix-hospital-expanded');
  });
});

// ─── PROGRAMS WORKFLOW ────────────────────────────────────────────────────────

test.describe('13 — Workflow: Programs Management', () => {
  test('step 1 — programs list', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/programs');
    await page.waitForLoadState('networkidle');
    await shot(page, '13-workflow-programs', '01-programs-list');
  });

  test('step 2 — program detail (if any)', async ({ page, context }) => {
    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/programs');
    await page.waitForLoadState('networkidle');
    // Click first program link/button if present
    const firstLink = page.getByRole('link').first();
    const firstBtn = page.getByRole('button', { name: /view|detail|program/i }).first();
    const hasLink = await firstLink.isVisible().catch(() => false);
    const hasBtn = await firstBtn.isVisible().catch(() => false);
    if (hasLink) {
      await firstLink.click().catch(() => {});
      await page.waitForLoadState('networkidle');
      await shot(page, '13-workflow-programs', '02-program-detail');
    } else if (hasBtn) {
      await firstBtn.click().catch(() => {});
      await page.waitForTimeout(600);
      await shot(page, '13-workflow-programs', '02-program-action');
    } else {
      await shot(page, '13-workflow-programs', '02-programs-no-items');
    }
  });
});
