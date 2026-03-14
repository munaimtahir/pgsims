import { expect, test } from '@playwright/test';

import { loginAs } from '../helpers/auth';

const APP_BASE_URL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
const SEEDED_RESEARCH_TITLE = 'E2E Baseline Research Project';

type AuthTokenResponse = { access: string };
type ResearchPayload = { id: number; status: string; title: string };

async function getToken(
  request: import('@playwright/test').APIRequestContext,
  username: string,
  password: string
): Promise<string> {
  const resp = await request.post(`${APP_BASE_URL}/api/auth/login/`, {
    data: { username, password },
  });
  expect(resp.ok(), `Auth failed for ${username}: ${await resp.text()}`).toBeTruthy();
  const payload = (await resp.json()) as AuthTokenResponse;
  return payload.access;
}

async function getResearch(
  request: import('@playwright/test').APIRequestContext,
  token: string
): Promise<ResearchPayload> {
  const resp = await request.get(`${APP_BASE_URL}/api/my/research/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(resp.ok(), `Could not load resident research: ${await resp.text()}`).toBeTruthy();
  return (await resp.json()) as ResearchPayload;
}

async function ensurePendingForSupervisorReview(
  request: import('@playwright/test').APIRequestContext
): Promise<ResearchPayload> {
  const pgToken = await getToken(request, 'e2e_pg', 'Pg123456!');
  let project = await getResearch(request, pgToken);

  if (project.status === 'DRAFT') {
    const submitResp = await request.post(`${APP_BASE_URL}/api/my/research/action/submit-to-supervisor/`, {
      headers: { Authorization: `Bearer ${pgToken}` },
      data: {},
    });
    expect(
      submitResp.ok(),
      `Could not transition draft research to submitted: ${await submitResp.text()}`
    ).toBeTruthy();
    project = (await submitResp.json()) as ResearchPayload;
  }

  expect(
    project.status,
    `Research status must be SUBMITTED_TO_SUPERVISOR for workflow gate. Current: ${project.status}`
  ).toBe('SUBMITTED_TO_SUPERVISOR');

  return project;
}

test.describe('Workflow gate — stabilized contract-critical flows', () => {
  test('forgot-password submits via real UI path and returns success response', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.getByLabel('Email address').fill('e2e_pg@pgsims.local');
    await page.getByRole('button', { name: /send reset link/i }).click();

    await expect(page.getByText(/password reset email sent|if an account with that email exists/i)).toBeVisible({
      timeout: 15_000,
    });
  });

  test('supervisor approvals renders resident_name and supports supervisor-return flow', async ({
    context,
    page,
  }) => {
    await ensurePendingForSupervisorReview(page.request);

    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/research-approvals');

    await expect(page.getByRole('heading', { name: 'Research Approvals' })).toBeVisible();

    const pendingCard = page.locator('div.bg-white').filter({ hasText: SEEDED_RESEARCH_TITLE }).first();
    await expect(pendingCard).toBeVisible({ timeout: 15_000 });
    await expect(pendingCard.getByText(/Resident:\s*E2E PG/i)).toBeVisible();

    await pendingCard.getByRole('button', { name: /return with feedback/i }).click();
    await pendingCard.getByPlaceholder(/Provide feedback reason/i).fill(
      'Please refine objectives and resubmit.'
    );
    await pendingCard.getByRole('button', { name: /send return/i }).click();

    await expect(page.getByText(/Returned with feedback/i)).toBeVisible({ timeout: 15_000 });
    await expect(pendingCard).not.toBeVisible({ timeout: 15_000 });
    await expect(page.getByText(/No pending research submissions\./i)).toBeVisible({ timeout: 15_000 });
  });

  test('resident dashboard shows canonical eligibility reasons in browser', async ({ context, page }) => {
    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident');

    await expect(page.getByRole('heading', { name: 'My Training Dashboard' })).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByText(/Exam Eligibility/i)).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText('Synopsis not yet approved by supervisor').first()).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByText('Thesis not yet submitted').first()).toBeVisible({
      timeout: 15_000,
    });
  });
});
