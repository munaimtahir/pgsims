import { expect, test } from '@playwright/test';
import { loginAs } from '../helpers/auth';

test('utrmc admin can build userbase graph and resident scope is enforced', async ({ page, context }) => {
  test.setTimeout(180000);
  await loginAs(context, page, 'admin');

  const suffix = `e2e-${Date.now()}`;
  const hospitalName = `Hospital ${suffix}`;
  const departmentName = `Department ${suffix}`;
  const uniqueCode = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const departmentCode = `D${uniqueCode.slice(-8)}`;
  const supervisorUsername = `sup_${suffix}`;
  const residentUsername = `res_${suffix}`;
  const supervisorPassword = 'Supervisor123!';
  const residentPassword = 'Resident123!';

  await page.goto('/dashboard/utrmc');
  const adminAccessToken = await page.evaluate(() => {
    const raw = localStorage.getItem('auth-storage');
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
    return parsed.state?.accessToken ?? null;
  });
  expect(adminAccessToken).toBeTruthy();
  const adminAuthHeaders = { Authorization: `Bearer ${adminAccessToken as string}` };

  const createHospitalResponse = await page.request.post('/api/hospitals/', {
    headers: adminAuthHeaders,
    data: { name: hospitalName, code: `H${uniqueCode.slice(-8)}`, active: true },
  });
  expect(createHospitalResponse.ok()).toBeTruthy();
  const hospitalPayload = (await createHospitalResponse.json()) as { id: number };
  const hospitalId = hospitalPayload.id;
  expect(hospitalId).toBeGreaterThan(0);

  const createDepartmentResponse = await page.request.post('/api/departments/', {
    headers: adminAuthHeaders,
    data: { name: departmentName, code: departmentCode, active: true },
  });
  expect(createDepartmentResponse.ok()).toBeTruthy();
  const departmentPayload = (await createDepartmentResponse.json()) as { id: number };
  const departmentId = departmentPayload.id;
  expect(departmentId).toBeGreaterThan(0);

  await page.context().clearCookies();
  await loginAs(context, page, 'utrmc_admin');

  await page.goto('/dashboard/utrmc/matrix');
  const utrmcAccessToken = await page.evaluate(() => {
    const raw = localStorage.getItem('auth-storage');
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { state?: { accessToken?: string } };
    return parsed.state?.accessToken ?? null;
  });
  expect(utrmcAccessToken).toBeTruthy();
  const utrmcAuthHeaders = { Authorization: `Bearer ${utrmcAccessToken as string}` };
  await expect(page.getByRole('heading', { name: 'Hospital\u2013Department Matrix' })).toBeVisible();
  const createMatrixResponse = await page.request.post('/api/hospital-departments/', {
    headers: utrmcAuthHeaders,
    data: { hospital_id: hospitalId, department_id: departmentId, active: true },
  });
  expect(createMatrixResponse.ok()).toBeTruthy();
  const matrixPayload = (await createMatrixResponse.json()) as { id: number };
  const hospitalDepartmentId = matrixPayload.id;
  expect(hospitalDepartmentId).toBeGreaterThan(0);

  const trainingStart = new Date().toISOString().slice(0, 10);
  const supervisorResponse = await page.request.post('/api/users/', {
    headers: utrmcAuthHeaders,
    data: {
      username: supervisorUsername,
      email: `${supervisorUsername}@example.com`,
      password: supervisorPassword,
      first_name: 'Sup',
      last_name: 'User',
      role: 'supervisor',
      specialty: 'medicine',
      is_active: true,
      staff_profile: { designation: 'Supervisor', active: true },
    },
  });
  expect(supervisorResponse.ok()).toBeTruthy();
  const supervisorPayload = (await supervisorResponse.json()) as { id: number };
  const supervisorId = supervisorPayload.id;
  expect(supervisorId).toBeGreaterThan(0);

  const residentResponse = await page.request.post('/api/users/', {
    headers: utrmcAuthHeaders,
    data: {
      username: residentUsername,
      email: `${residentUsername}@example.com`,
      password: residentPassword,
      first_name: 'Res',
      last_name: 'User',
      role: 'resident',
      specialty: 'medicine',
      year: '1',
      is_active: true,
      resident_profile: { training_start: trainingStart, training_level: '1', active: true },
    },
  });
  expect(residentResponse.ok()).toBeTruthy();
  const residentPayload = (await residentResponse.json()) as { id: number };
  const residentId = residentPayload.id;
  expect(residentId).toBeGreaterThan(0);

  const supervisorMembershipResponse = await page.request.post('/api/department-memberships/', {
    headers: utrmcAuthHeaders,
    data: {
      user_id: supervisorId,
      department_id: departmentId,
      member_type: 'supervisor',
      is_primary: true,
      start_date: trainingStart,
      active: true,
    },
  });
  expect(supervisorMembershipResponse.ok()).toBeTruthy();

  const residentMembershipResponse = await page.request.post('/api/department-memberships/', {
    headers: utrmcAuthHeaders,
    data: {
      user_id: residentId,
      department_id: departmentId,
      member_type: 'resident',
      is_primary: true,
      start_date: trainingStart,
      active: true,
    },
  });
  expect(residentMembershipResponse.ok()).toBeTruthy();

  const hospitalAssignmentResponse = await page.request.post('/api/hospital-assignments/', {
    headers: utrmcAuthHeaders,
    data: {
      user_id: residentId,
      hospital_department_id: hospitalDepartmentId,
      assignment_type: 'primary_training',
      start_date: trainingStart,
      active: true,
    },
  });
  expect(hospitalAssignmentResponse.ok()).toBeTruthy();

  const supervisionResponse = await page.request.post('/api/supervision-links/', {
    headers: utrmcAuthHeaders,
    data: {
      supervisor_user_id: supervisorId,
      resident_user_id: residentId,
      department_id: departmentId,
      start_date: new Date().toISOString().slice(0, 10),
      active: true,
    },
  });
  expect(supervisionResponse.ok()).toBeTruthy();

  const hodResponse = await page.request.post('/api/hod-assignments/', {
    headers: utrmcAuthHeaders,
    data: {
      department_id: departmentId,
      hod_user_id: supervisorId,
      start_date: new Date().toISOString().slice(0, 10),
      active: true,
    },
  });
  expect(hodResponse.ok()).toBeTruthy();

  await page.goto(`/dashboard/utrmc/departments/${departmentId}/roster`);
  await expect(page.getByText(departmentName)).toBeVisible();
  await expect(page.locator('li', { hasText: 'Sup User' })).toBeVisible();
  await expect(page.locator('li', { hasText: 'Res User' })).toBeVisible();

  await page.context().clearCookies();
  const residentLoginResponse = await page.request.post('/api/auth/login/', {
    data: { username: residentUsername, password: residentPassword },
  });
  expect(residentLoginResponse.ok()).toBeTruthy();
  const residentAuth = (await residentLoginResponse.json()) as {
    access: string;
    refresh: string;
    user: { role: string; username: string; id: number; email: string; first_name: string; last_name: string; full_name: string };
  };
  const appBaseURL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:8082';
  await context.addCookies([
    { name: 'pgsims_access_token', value: residentAuth.access, url: appBaseURL },
    { name: 'pgsims_user_role', value: residentAuth.user.role, url: appBaseURL },
    { name: 'pgsims_access_exp', value: String(Math.floor(Date.now() / 1000) + 3600), url: appBaseURL },
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
  }, residentAuth);

  await page.goto('/dashboard/pg');
  await page.waitForURL(/\/dashboard\/pg/);

  await page.goto('/dashboard/utrmc/users');
  await page.waitForURL(/\/dashboard\/pg/);

  await page.goto(`/dashboard/pg/departments/${departmentId}/roster`);
  await expect(page.getByRole('heading', { name: 'Department Roster' })).toBeVisible();
  await expect(page.getByText(departmentName)).toBeVisible();
});
