import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test('utrmc admin can build userbase graph and resident scope is enforced', async ({ page, context }) => {
  await loginAs(context, page, 'utrmc_admin');

  const suffix = `e2e-${Date.now()}`;
  const hospitalName = `Hospital ${suffix}`;
  const departmentName = `Department ${suffix}`;
  const departmentCode = `D${Date.now().toString().slice(-5)}`;
  const supervisorUsername = `sup_${suffix}`;
  const residentUsername = `res_${suffix}`;
  const supervisorPassword = 'Supervisor123!';
  const residentPassword = 'Resident123!';

  await page.goto('/dashboard/utrmc/hospitals');
  const userbaseUiPresent = await page
    .getByPlaceholder('Hospital name')
    .isVisible({ timeout: 5000 })
    .catch(() => false);
  test.skip(!userbaseUiPresent, 'Userbase UTRMC pages are not available on the configured base URL.');
  await page.getByPlaceholder('Hospital name').fill(hospitalName);
  await page.getByPlaceholder('Code').fill(`H${Date.now().toString().slice(-4)}`);
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByRole('cell', { name: hospitalName })).toBeVisible();

  await page.goto('/dashboard/utrmc/departments');
  await page.getByPlaceholder('Department name').fill(departmentName);
  await page.getByPlaceholder('Code').fill(departmentCode);
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByRole('cell', { name: departmentName })).toBeVisible();

  const departmentsResp = await page.request.get(`/api/departments/?search=${encodeURIComponent(departmentCode)}`);
  const departmentsJson = (await departmentsResp.json()) as { results?: Array<{ id: number; code: string }> };
  const departmentId = departmentsJson.results?.[0]?.id;
  expect(departmentId).toBeTruthy();

  const hospitalsResp = await page.request.get('/api/hospitals/?search=' + encodeURIComponent(hospitalName));
  const hospitalsJson = (await hospitalsResp.json()) as { results?: Array<{ id: number; name: string }> };
  const hospitalId = hospitalsJson.results?.find((row) => row.name === hospitalName)?.id;
  expect(hospitalId).toBeTruthy();

  await page.goto('/dashboard/utrmc/matrix');
  await page.locator('select').nth(0).selectOption(String(hospitalId));
  await page.locator('select').nth(1).selectOption(String(departmentId));
  await page.getByRole('button', { name: 'Add Mapping' }).click();
  await expect(page.getByRole('cell', { name: hospitalName })).toBeVisible();
  await expect(page.getByRole('cell', { name: departmentName })).toBeVisible();

  await page.goto('/dashboard/utrmc/users/new');
  await page.getByPlaceholder('Username').fill(supervisorUsername);
  await page.getByPlaceholder('Email').fill(`${supervisorUsername}@example.com`);
  await page.getByPlaceholder('Password').fill(supervisorPassword);
  await page.getByPlaceholder('First name').fill('Sup');
  await page.getByPlaceholder('Last name').fill('User');
  await page.locator('select').first().selectOption('supervisor');
  await page.getByPlaceholder('Specialty').fill('medicine');
  await page.getByRole('button', { name: 'Create User' }).click();
  await page.waitForURL(/\/dashboard\/utrmc\/users\/\d+$/);
  const supervisorId = Number(page.url().split('/').pop());
  expect(supervisorId).toBeGreaterThan(0);

  await page.locator('select').nth(2).selectOption(String(departmentId));
  await page.locator('select').nth(3).selectOption('supervisor');
  await page.getByRole('button', { name: 'Assign Department' }).click();

  await page.goto('/dashboard/utrmc/users/new');
  await page.getByPlaceholder('Username').fill(residentUsername);
  await page.getByPlaceholder('Email').fill(`${residentUsername}@example.com`);
  await page.getByPlaceholder('Password').fill(residentPassword);
  await page.getByPlaceholder('First name').fill('Res');
  await page.getByPlaceholder('Last name').fill('User');
  await page.locator('select').first().selectOption('resident');
  await page.getByPlaceholder('Specialty').fill('medicine');
  await page.getByPlaceholder('Year/Level').fill('1');
  await page.getByPlaceholder('Training start (YYYY-MM-DD)').fill(new Date().toISOString().slice(0, 10));
  await page.getByRole('button', { name: 'Create User' }).click();
  await page.waitForURL(/\/dashboard\/utrmc\/users\/\d+$/);
  const residentId = Number(page.url().split('/').pop());
  expect(residentId).toBeGreaterThan(0);

  await page.locator('select').nth(2).selectOption(String(departmentId));
  await page.locator('select').nth(3).selectOption('resident');
  await page.getByRole('button', { name: 'Assign Department' }).click();

  const matrixResp = await page.request.get(
    `/api/hospital-departments/?hospital=${hospitalId}&department=${departmentId}`
  );
  const matrixJson = (await matrixResp.json()) as { results?: Array<{ id: number }> };
  const hospitalDepartmentId = matrixJson.results?.[0]?.id;
  expect(hospitalDepartmentId).toBeTruthy();

  await page.locator('select').nth(4).selectOption(String(hospitalDepartmentId));
  await page.locator('select').nth(5).selectOption('primary_training');
  await page.getByRole('button', { name: 'Assign Site' }).click();

  await page.goto('/dashboard/utrmc/linking/supervision');
  await page.locator('select').nth(0).selectOption(String(supervisorId));
  await page.locator('select').nth(1).selectOption(String(residentId));
  await page.locator('select').nth(2).selectOption(String(departmentId));
  await page.getByRole('button', { name: 'Create Link' }).click();
  await expect(page.getByRole('cell', { name: /Sup User/i })).toBeVisible();

  await page.goto('/dashboard/utrmc/linking/hod');
  await page.locator('select').nth(0).selectOption(String(departmentId));
  await page.locator('select').nth(1).selectOption(String(supervisorId));
  await page.getByRole('button', { name: 'Assign HOD' }).click();
  await expect(page.getByRole('cell', { name: departmentName })).toBeVisible();

  await page.goto(`/dashboard/utrmc/departments/${departmentId}/roster`);
  await expect(page.getByText(departmentName)).toBeVisible();
  await expect(page.getByText('Sup User')).toBeVisible();
  await expect(page.getByText('Res User')).toBeVisible();

  await page.context().clearCookies();
  await page.goto('/login');
  await page.getByLabel('Username').fill(residentUsername);
  await page.getByLabel('Password').fill(residentPassword);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL(/\/dashboard\/pg/);

  await page.goto('/dashboard/utrmc/users');
  await page.waitForURL(/\/dashboard\/pg/);

  await page.goto(`/dashboard/pg/departments/${departmentId}/roster`);
  await expect(page.getByRole('heading', { name: 'Department Roster' })).toBeVisible();
  await expect(page.getByText(departmentName)).toBeVisible();
});
