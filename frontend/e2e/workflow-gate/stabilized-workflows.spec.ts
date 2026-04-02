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

function toIsoDate(value: Date): string {
  return value.toISOString().slice(0, 10);
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

  test('resident leave draft can be submitted and approved from supervisor dashboard', async ({
    context,
    page,
  }) => {
    test.setTimeout(60_000);
    const leaveReason = `Workflow leave ${Date.now()}`;

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    await expect(page.getByRole('heading', { name: 'My Schedule' })).toBeVisible({ timeout: 15_000 });
    await page.getByLabel('Leave Type').selectOption('study');
    await page.getByLabel('Start Date').fill('2026-04-10');
    await page.getByLabel('End Date').fill('2026-04-12');
    await page.getByLabel('Reason').fill(leaveReason);
    await page.getByRole('button', { name: 'Save Draft' }).click();

    await expect(page.getByText(/Leave request saved as draft\./i)).toBeVisible({ timeout: 15_000 });

    const residentLeaveCard = page.locator('div.border').filter({ hasText: leaveReason }).first();
    await expect(residentLeaveCard).toBeVisible({ timeout: 15_000 });
    await residentLeaveCard.getByRole('button', { name: /submit for review/i }).click();
    await expect(page.getByText(/Leave request submitted for review\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');

    const supervisorLeaveCard = page.locator('div.bg-white').filter({ hasText: leaveReason }).first();
    await expect(supervisorLeaveCard).toBeVisible({ timeout: 15_000 });
    await supervisorLeaveCard.getByRole('button', { name: 'Approve' }).click();
    await expect(page.getByText(/Leave request approved\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    const approvedLeaveCard = page.locator('div.border').filter({ hasText: leaveReason }).first();
    await expect(approvedLeaveCard).toBeVisible({ timeout: 15_000 });
    await expect(approvedLeaveCard.getByText('APPROVED')).toBeVisible({ timeout: 15_000 });
  });

  test('rotation workflow closes across UTRMC overview, resident schedule, and supervisor dashboard', async ({
    context,
    page,
  }) => {
    test.setTimeout(90_000);
    const uniqueSuffix = `${Date.now()}`;
    const startDate = new Date(Date.UTC(2026, 6, 1));
    startDate.setUTCDate(startDate.getUTCDate() + Number(uniqueSuffix.slice(-2)));
    const endDate = new Date(startDate);
    endDate.setUTCDate(endDate.getUTCDate() + 28);
    const rotationNote = `Workflow rotation ${uniqueSuffix}`;

    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');

    await expect(page.getByRole('heading', { name: 'UTRMC Overview' })).toBeVisible({ timeout: 15_000 });
    const residentSelect = page.getByLabel('Resident');
    const residentOptionValue = await residentSelect.locator('option').evaluateAll((options) => {
      const match = options.find((option) => option.textContent?.includes('E2E PG'));
      return match instanceof HTMLOptionElement ? match.value : '';
    });
    expect(residentOptionValue).toBeTruthy();
    await residentSelect.selectOption(residentOptionValue);

    const placementSelect = page.getByLabel('Placement');
    const placementOptionValue = await placementSelect.locator('option').nth(1).getAttribute('value');
    expect(placementOptionValue).toBeTruthy();
    await placementSelect.selectOption(placementOptionValue!);
    await page.getByLabel('Start Date').fill(toIsoDate(startDate));
    await page.getByLabel('End Date').fill(toIsoDate(endDate));
    await page.getByLabel('Notes').fill(rotationNote);
    await page.getByRole('button', { name: 'Create Rotation Draft' }).click();

    await expect(page.getByText(/Rotation draft created\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    const residentRotationCard = page.locator('div.border').filter({ hasText: rotationNote }).first();
    await expect(residentRotationCard).toBeVisible({ timeout: 15_000 });
    await expect(residentRotationCard.getByText('DRAFT')).toBeVisible({ timeout: 15_000 });
    await residentRotationCard.getByRole('button', { name: /submit for review/i }).click();
    await expect(page.getByText(/Rotation submitted for supervisor review\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor');

    const supervisorRotationCard = page.locator('div.bg-white').filter({ hasText: rotationNote }).first();
    await expect(supervisorRotationCard).toBeVisible({ timeout: 15_000 });
    await supervisorRotationCard.getByRole('button', { name: /approve rotation/i }).click();
    await expect(page.getByText(/Rotation approved\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc');

    const approvedRotationCard = page.locator('div.bg-white').filter({ hasText: rotationNote }).first();
    await expect(approvedRotationCard).toBeVisible({ timeout: 15_000 });
    await approvedRotationCard.getByRole('button', { name: /activate rotation/i }).click();
    await expect(page.getByText(/Rotation activated\./i)).toBeVisible({ timeout: 15_000 });

    const activeRotationCard = page.locator('div.bg-white').filter({ hasText: rotationNote }).first();
    await expect(activeRotationCard.getByText('ACTIVE')).toBeVisible({ timeout: 15_000 });
    await activeRotationCard.getByRole('button', { name: /mark complete/i }).click();
    await expect(page.getByText(/Rotation completed\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/schedule');

    const completedRotationCard = page.locator('div.border').filter({ hasText: rotationNote }).first();
    await expect(completedRotationCard).toBeVisible({ timeout: 15_000 });
    await expect(completedRotationCard.getByText('COMPLETED')).toBeVisible({ timeout: 15_000 });
  });

  test('posting workflow remains truthful from resident submission through UTRMC completion', async ({
    context,
    page,
  }) => {
    test.setTimeout(90_000);
    const uniqueSuffix = `${Date.now()}`;
    const startDate = new Date(Date.UTC(2026, 8, 1));
    startDate.setUTCDate(startDate.getUTCDate() + Number(uniqueSuffix.slice(-2)));
    const endDate = new Date(startDate);
    endDate.setUTCDate(endDate.getUTCDate() + 14);
    const institutionName = `Workflow Posting ${uniqueSuffix}`;
    const postingNotes = `Posting objective ${uniqueSuffix}`;

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/postings');

    await page.getByRole('button', { name: /\+ request posting/i }).click();
    await expect(page.getByRole('heading', { name: 'New Posting Request' })).toBeVisible({ timeout: 15_000 });
    const postingForm = page.locator('form').filter({ hasText: 'New Posting Request' });
    await postingForm.getByPlaceholder('Name of the hosting institution').fill(institutionName);
    await postingForm.getByPlaceholder('e.g. Riyadh').fill('Lahore');
    await postingForm.locator('input[type="date"]').nth(0).fill(toIsoDate(startDate));
    await postingForm.locator('input[type="date"]').nth(1).fill(toIsoDate(endDate));
    await postingForm.getByPlaceholder('Optional — reason or clinical objectives for this posting').fill(postingNotes);
    await postingForm.getByRole('button', { name: 'Create Request' }).click();

    await expect(page.getByText(/Posting request submitted for review\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'utrmc_admin');
    await page.goto('/dashboard/utrmc/postings');

    const postingCard = page.locator('div.bg-white').filter({ hasText: institutionName }).first();
    await expect(postingCard).toBeVisible({ timeout: 15_000 });
    await postingCard.getByRole('button', { name: 'Approve' }).click();
    await expect(page.getByText(/Posting approved successfully\./i)).toBeVisible({ timeout: 15_000 });

    const approvedPostingCard = page.locator('div.bg-white').filter({ hasText: institutionName }).first();
    await expect(approvedPostingCard.getByRole('button', { name: /mark complete/i })).toBeVisible({ timeout: 15_000 });
    await approvedPostingCard.getByRole('button', { name: /mark complete/i }).click();
    await expect(page.getByText(/Posting completed successfully\./i)).toBeVisible({ timeout: 15_000 });

    await loginAs(context, page, 'pg');
    await page.goto('/dashboard/resident/postings');

    const residentPostingCard = page.locator('div.bg-white').filter({ hasText: institutionName }).first();
    await expect(residentPostingCard).toBeVisible({ timeout: 15_000 });
    await expect(residentPostingCard.getByText('Completed')).toBeVisible({ timeout: 15_000 });
  });
});
