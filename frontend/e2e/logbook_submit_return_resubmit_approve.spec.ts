import { expect, test, type Page } from '@playwright/test';
import { seedAuth } from './helpers/auth';

type MockEntry = {
  id: number;
  case_title: string;
  date: string;
  location_of_activity: string;
  patient_history_summary: string;
  management_action: string;
  topic_subtopic: string;
  status: 'draft' | 'pending' | 'returned' | 'approved' | 'rejected';
  created_at: string;
  updated_at: string;
  submitted_to_supervisor_at: string | null;
  submitted_at: string | null;
  supervisor_feedback: string | null;
  feedback: string | null;
  verified_at: string | null;
};

test.describe('Logbook Core Workflow', () => {
  test('PG submit -> supervisor return -> PG sees feedback -> resubmit -> approve -> edit blocked', async ({
    page,
    context,
  }) => {
    let nextId = 1;
    let entries: MockEntry[] = [];
    const promptReplies: string[] = [];

    page.on('dialog', async (dialog) => {
      if (dialog.type() === 'confirm') {
        await dialog.accept();
        return;
      }
      if (dialog.type() === 'prompt') {
        await dialog.accept(promptReplies.shift() ?? '');
        return;
      }
      await dialog.dismiss();
    });

    await mockLogbookApi(page, () => entries, (next) => (entries = next), () => nextId++);

    await seedAuth(context, page, 'pg');
    await page.goto('/dashboard/pg/logbook');
    await expect(page.getByText(/no logbook entries yet/i)).toBeVisible();

    await page.getByTestId('logbook-form-case-title').fill('Appendectomy follow-up');
    await page.getByTestId('logbook-form-date').fill('2026-02-26');
    await page.getByTestId('logbook-form-location').fill('Ward');
    await page.getByTestId('logbook-form-history').fill('Patient improving post-op.');
    await page.getByTestId('logbook-form-management').fill('Continue antibiotics and observe.');
    await page.getByTestId('logbook-form-topic').fill('Surgery / Post-op');
    await page.getByTestId('logbook-save-button').click();

    const entryId = 1;
    await expect(page.getByText(/draft logbook entry created successfully/i)).toBeVisible();
    await expect(page.getByTestId(`logbook-status-${entryId}`)).toHaveText('Draft');

    await page.getByTestId(`logbook-submit-${entryId}`).click();
    await expect(page.getByText(/submitted for supervisor review/i)).toBeVisible();

    await seedAuth(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/logbooks');
    await expect(page.getByTestId(`supervisor-logbook-status-${entryId}`)).toHaveText('Submitted');

    promptReplies.push('Please add more detail.');
    await page.getByTestId(`supervisor-return-${entryId}`).click();
    await expect(page.getByText(/returned successfully/i)).toBeVisible();

    await seedAuth(context, page, 'pg');
    await page.goto('/dashboard/pg/logbook');
    await expect(page.getByTestId(`logbook-status-${entryId}`)).toHaveText('Returned');
    await expect(page.getByTestId(`logbook-feedback-${entryId}`)).toContainText('Please add more detail.');

    await page.getByTestId(`logbook-edit-${entryId}`).click();
    await page.getByTestId('logbook-form-management').fill('Updated management action with dosing detail.');
    await page.getByTestId('logbook-save-button').click();

    await page.getByTestId(`logbook-submit-${entryId}`).click();
    await expect(page.getByText(/submitted for supervisor review/i)).toBeVisible();

    await seedAuth(context, page, 'supervisor');
    await page.goto('/dashboard/supervisor/logbooks');
    promptReplies.push('Looks good now.');
    await page.getByTestId(`supervisor-approve-${entryId}`).click();
    await expect(page.getByText(/approved successfully/i)).toBeVisible();

    await seedAuth(context, page, 'pg');
    await page.goto('/dashboard/pg/logbook');
    await expect(page.getByTestId(`logbook-status-${entryId}`)).toHaveText('Approved');
    await expect(page.getByTestId(`logbook-edit-${entryId}`)).toHaveCount(0);
  });
});

async function mockLogbookApi(
  page: Page,
  getEntries: () => MockEntry[],
  setEntries: (entries: MockEntry[]) => void,
  nextId: () => number
) {
  const now = () => new Date().toISOString();

  const pgListPayload = () => ({ count: getEntries().length, results: getEntries().map((e) => ({ ...e })) });
  const pendingPayload = () => ({
    count: getEntries().filter((e) => e.status === 'pending').length,
    results: getEntries()
      .filter((e) => e.status === 'pending')
      .map((e) => ({
        id: e.id,
        case_title: e.case_title,
        date: e.date,
        user: { id: 10, username: 'pg', full_name: 'PG User' },
        rotation: { id: 1, department: 'Surgery' },
        submitted_at: e.submitted_at,
        status: e.status,
        feedback: e.feedback,
        supervisor_feedback: e.supervisor_feedback,
      })),
  });

  await page.route('**/api/logbook/my/', async (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      await route.fulfill({ json: pgListPayload() });
      return;
    }
    if (method === 'POST') {
      const body = (await route.request().postDataJSON()) as Record<string, string>;
      const entry: MockEntry = {
        id: nextId(),
        case_title: body.case_title,
        date: body.date,
        location_of_activity: body.location_of_activity,
        patient_history_summary: body.patient_history_summary,
        management_action: body.management_action,
        topic_subtopic: body.topic_subtopic,
        status: 'draft',
        created_at: now(),
        updated_at: now(),
        submitted_to_supervisor_at: null,
        submitted_at: null,
        supervisor_feedback: null,
        feedback: null,
        verified_at: null,
      };
      setEntries([entry, ...getEntries()]);
      await route.fulfill({ json: entry });
      return;
    }
    await route.fallback();
  });

  await page.route(/\/api\/logbook\/my\/\d+\/submit\/$/, async (route) => {
    const id = Number(route.request().url().match(/\/my\/(\d+)\/submit\//)?.[1]);
    setEntries(
      getEntries().map((e) =>
        e.id === id
          ? { ...e, status: 'pending', submitted_to_supervisor_at: now(), submitted_at: now(), updated_at: now() }
          : e
      )
    );
    await route.fulfill({ json: getEntries().find((e) => e.id === id) });
  });

  await page.route(/\/api\/logbook\/my\/\d+\/$/, async (route) => {
    if (route.request().method() !== 'PATCH') {
      await route.fallback();
      return;
    }
    const id = Number(route.request().url().match(/\/my\/(\d+)\/$/)?.[1]);
    const patch = (await route.request().postDataJSON()) as Record<string, string>;
    setEntries(getEntries().map((e) => (e.id === id ? { ...e, ...patch, updated_at: now() } : e)));
    await route.fulfill({ json: getEntries().find((e) => e.id === id) });
  });

  await page.route('**/api/logbook/pending/', async (route) => {
    await route.fulfill({ json: pendingPayload() });
  });

  await page.route(/\/api\/logbook\/\d+\/verify\/$/, async (route) => {
    const id = Number(route.request().url().match(/\/logbook\/(\d+)\/verify\//)?.[1]);
    const body = (await route.request().postDataJSON()) as { action?: string; feedback?: string };
    const action = body.action ?? 'approved';
    const nextStatus = action === 'returned' ? 'returned' : action === 'rejected' ? 'rejected' : 'approved';

    setEntries(
      getEntries().map((e) =>
        e.id === id
          ? {
              ...e,
              status: nextStatus,
              supervisor_feedback: body.feedback || null,
              feedback: body.feedback || null,
              verified_at: nextStatus === 'approved' ? now() : null,
              updated_at: now(),
            }
          : e
      )
    );

    const entry = getEntries().find((e) => e.id === id)!;
    await route.fulfill({
      json: {
        id: entry.id,
        case_title: entry.case_title,
        status: entry.status,
        supervisor_feedback: entry.supervisor_feedback,
        feedback: entry.feedback,
        verified_at: entry.verified_at,
      },
    });
  });
}
