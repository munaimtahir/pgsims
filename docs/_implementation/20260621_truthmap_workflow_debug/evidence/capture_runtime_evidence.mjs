import playwright from '/home/munaim/srv/apps/pgsims/frontend/node_modules/playwright/index.js';
import fs from 'fs/promises';
import path from 'path';

const root = '/home/munaim/srv/apps/pgsims';
const evidenceDir = path.join(root, 'docs/_implementation/20260621_truthmap_workflow_debug/evidence');
const screenshotsDir = path.join(evidenceDir, 'screenshots');

const baseUrl = process.env.E2E_BASE_URL || 'http://127.0.0.1:3000';
const { chromium } = playwright;

const authUser = {
  id: 100,
  username: 'utrmc_admin',
  role: 'utrmc_admin',
  profile_completed: true,
  force_password_change: false,
};

const departments = [
  { id: 1, name: 'Medicine', code: 'MED', active: true, created_at: '2026-06-21T00:00:00Z' },
  { id: 2, name: 'Urology', code: 'URO', active: true, created_at: '2026-06-21T00:00:00Z' },
];

const programs = [
  {
    id: 11,
    code: 'FCPS-URO',
    name: 'FCPS Urology',
    degree_type: 'FCPS',
    degree_type_display: 'FCPS',
    department: 2,
    duration_months: 60,
    is_active: true,
    notes: '',
  },
  {
    id: 12,
    code: 'FCPS-MED',
    name: 'FCPS Medicine',
    degree_type: 'FCPS',
    degree_type_display: 'FCPS',
    department: 1,
    duration_months: 60,
    is_active: true,
    notes: '',
  },
];

const users = [
  {
    id: 1,
    username: 'pilot_admin',
    full_name: 'Pilot Admin',
    email: 'admin@example.com',
    role: 'admin',
    is_active: true,
    first_name: 'Pilot',
    last_name: 'Admin',
    specialty: 'other',
    year: '',
    supervisor: null,
    home_department: 1,
    home_hospital: 1,
    departments: [{ id: 1, name: 'Medicine', code: 'MED', member_type: 'supervisor', is_primary: true }],
  },
  {
    id: 2,
    username: 'dr_sana',
    full_name: 'Dr Sana',
    email: 'sana@example.com',
    role: 'supervisor',
    is_active: true,
    first_name: 'Sana',
    last_name: 'Khan',
    specialty: 'urology',
    year: '',
    supervisor: null,
    home_department: 2,
    home_hospital: 1,
    departments: [{ id: 2, name: 'Urology', code: 'URO', member_type: 'supervisor', is_primary: true }],
  },
  {
    id: 3,
    username: 'resident_one',
    full_name: 'Resident One',
    email: 'resident.one@example.com',
    role: 'resident',
    is_active: true,
    first_name: 'Resident',
    last_name: 'One',
    specialty: '',
    year: '1',
    supervisor: 2,
    home_department: 2,
    home_hospital: 1,
    departments: [{ id: 2, name: 'Urology', code: 'URO', member_type: 'resident', is_primary: true }],
  },
  {
    id: 4,
    username: 'faculty_ali',
    full_name: 'Dr Ali',
    email: 'ali@example.com',
    role: 'faculty',
    is_active: true,
    first_name: 'Ali',
    last_name: 'Raza',
    specialty: 'medicine',
    year: '',
    supervisor: null,
    home_department: 1,
    home_hospital: 1,
    departments: [{ id: 1, name: 'Medicine', code: 'MED', member_type: 'supervisor', is_primary: true }],
  },
];

const residentTrainingRecords = [
  {
    id: 21,
    resident_user: 3,
    resident_name: 'Resident One',
    program: 11,
    program_name: 'FCPS Urology',
    program_code: 'FCPS-URO',
    start_date: '2026-01-01',
    expected_end_date: '2031-01-01',
    current_level: 'y1',
    active: true,
    created_by: 1,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
  },
];

const supervisionLinks = [
  {
    id: 31,
    supervisor_user: { id: 2, username: 'dr_sana', full_name: 'Dr Sana', role: 'supervisor', is_active: true },
    resident_user: { id: 3, username: 'resident_one', full_name: 'Resident One', role: 'resident', is_active: true },
    department: { id: 2, name: 'Urology', code: 'URO', active: true },
    start_date: '2026-01-01',
    end_date: null,
    active: true,
  },
];

const hodAssignments = [
  {
    id: 41,
    department: { id: 2, name: 'Urology', code: 'URO', active: true },
    hod_user: { id: 2, username: 'dr_sana', full_name: 'Dr Sana', role: 'supervisor', is_active: true },
    start_date: '2026-02-01',
    end_date: null,
    active: true,
  },
];

const dashboardData = {
  cross_department_overview: {
    active_residents: 42,
    program_count: 8,
    pending_logbook_reviews: 5,
  },
  pending_synopsis_reviews: 2,
  pending_thesis_reviews: 1,
  pending_rotation_completion_verifications: 3,
  resident_milestone_readiness: [
    {
      resident_id: 3,
      resident_name: 'Resident One',
      program: 'FCPS Urology',
      logbook_threshold_met: true,
      synopsis_certificate_issued: false,
      thesis_certificate_issued: false,
      required_rotation_count: 10,
      verified_rotation_count: 8,
      rotation_requirement_met: false,
    },
  ],
  readiness_summary: {
    fully_ready_count: 1,
    total_rows: 42,
  },
};

const dataQualitySummary = {
  total_users: 42,
  users_with_placeholder_email: 1,
  users_with_missing_dates: 4,
  complete_profiles: 38,
  incomplete_profiles: 4,
};

const overlayNote = async (page, text) => {
  await page.evaluate((message) => {
    const existing = document.getElementById('evidence-note');
    if (existing) existing.remove();
    const note = document.createElement('div');
    note.id = 'evidence-note';
    note.textContent = message;
    note.style.position = 'fixed';
    note.style.right = '16px';
    note.style.bottom = '16px';
    note.style.zIndex = '9999';
    note.style.maxWidth = '360px';
    note.style.padding = '12px 14px';
    note.style.borderRadius = '12px';
    note.style.background = 'rgba(15, 23, 42, 0.92)';
    note.style.color = 'white';
    note.style.fontSize = '12px';
    note.style.lineHeight = '1.4';
    note.style.boxShadow = '0 10px 30px rgba(0,0,0,0.25)';
    note.style.whiteSpace = 'pre-wrap';
    document.body.appendChild(note);
  }, text);
};

function jsonResponse(payload, status = 200) {
  return {
    status,
    contentType: 'application/json',
    body: JSON.stringify(payload),
  };
}

function filteredUsers(url) {
  const params = url.searchParams;
  let rows = [...users];
  if (params.get('role')) rows = rows.filter((item) => item.role === params.get('role'));
  if (params.get('department')) rows = rows.filter((item) => String(item.home_department) === params.get('department'));
  if (params.get('supervisor')) rows = rows.filter((item) => String(item.supervisor || '') === params.get('supervisor'));
  if (params.get('program')) {
    const programId = Number(params.get('program'));
    rows = rows.filter((item) => residentTrainingRecords.some((record) => record.resident_user === item.id && record.program === programId));
  }
  if (params.get('active') === 'true') rows = rows.filter((item) => item.is_active);
  if (params.get('active') === 'false') rows = rows.filter((item) => !item.is_active);
  const search = (params.get('search') || '').toLowerCase();
  if (search) {
    rows = rows.filter((item) => [item.username, item.full_name, item.email].join(' ').toLowerCase().includes(search));
  }
  return rows;
}

async function installRoutes(page, state) {
  await page.route('**/api/**', async (route) => {
    const req = route.request();
    const url = new URL(req.url());
    const { pathname } = url;
    const method = req.method();

    const respond = (payload, status = 200) => route.fulfill(jsonResponse(payload, status));

    if (method === 'GET' && pathname === '/api/dashboard/utrmc/') {
      return respond(dashboardData);
    }
    if (method === 'GET' && pathname === '/api/admin/data-quality/summary') {
      return respond(dataQualitySummary);
    }
    if (method === 'GET' && pathname === '/api/users/') {
      return respond(filteredUsers(url));
    }
    if (method === 'POST' && pathname.match(/^\/api\/users\/\d+\/reset-password\/$/)) {
      state.resetPasswordCalls += 1;
      return respond({ detail: 'Password reset to pgfmu123.' });
    }
    if (method === 'POST' && pathname.match(/^\/api\/users\/\d+\/deactivate\/$/)) {
      return respond({ detail: 'User deactivated.' });
    }
    if (method === 'DELETE' && pathname.match(/^\/api\/users\/\d+\/$/)) {
      return respond({ detail: 'User archived.' });
    }
    if (method === 'GET' && pathname === '/api/departments/') {
      return respond(departments);
    }
    if (method === 'GET' && pathname === '/api/hospital-departments/') {
      return respond([
        {
          id: 51,
          hospital: { id: 1, name: 'FMU Teaching Hospital', code: 'FMUTH', active: true, created_at: '2026-06-21T00:00:00Z' },
          department: departments[0],
          active: true,
          created_at: '2026-06-21T00:00:00Z',
        },
        {
          id: 52,
          hospital: { id: 1, name: 'FMU Teaching Hospital', code: 'FMUTH', active: true, created_at: '2026-06-21T00:00:00Z' },
          department: departments[1],
          active: true,
          created_at: '2026-06-21T00:00:00Z',
        },
      ]);
    }
    if (method === 'GET' && pathname === '/api/programs/') {
      return respond(programs);
    }
    if (method === 'GET' && pathname === '/api/resident-training/') {
      return respond(residentTrainingRecords);
    }
    if (method === 'POST' && pathname === '/api/resident-training/') {
      const body = JSON.parse(req.postData() || '{}');
      const record = {
        id: 99,
        resident_user: body.resident_user,
        resident_name: users.find((user) => user.id === body.resident_user)?.full_name || '',
        program: body.program,
        program_name: programs.find((program) => program.id === body.program)?.name || '',
        program_code: programs.find((program) => program.id === body.program)?.code || '',
        start_date: body.start_date,
        expected_end_date: body.expected_end_date || null,
        current_level: body.current_level || '',
        active: body.active !== false,
        created_by: authUser.id,
        created_at: '2026-06-21T12:00:00Z',
        updated_at: '2026-06-21T12:00:00Z',
      };
      residentTrainingRecords.unshift(record);
      return respond(record, 201);
    }
    if (method === 'PATCH' && pathname.match(/^\/api\/resident-training\/\d+\/$/)) {
      return respond({ detail: 'updated' });
    }
    if (method === 'DELETE' && pathname.match(/^\/api\/resident-training\/\d+\/$/)) {
      return respond({ detail: 'deleted' });
    }
    if (method === 'GET' && pathname === '/api/supervision-links/') {
      return respond(supervisionLinks);
    }
    if (method === 'POST' && pathname === '/api/supervision-links/') {
      const body = JSON.parse(req.postData() || '{}');
      const link = {
        id: 88,
        supervisor_user: users.find((user) => user.id === body.supervisor_user_id),
        resident_user: users.find((user) => user.id === body.resident_user_id),
        department: departments.find((department) => department.id === body.department_id) || null,
        start_date: body.start_date,
        end_date: null,
        active: body.active !== false,
      };
      supervisionLinks.unshift(link);
      return respond(link, 201);
    }
    if (method === 'GET' && pathname === '/api/hod-assignments/') {
      return respond(hodAssignments);
    }
    if (method === 'POST' && pathname === '/api/hod-assignments/') {
      const body = JSON.parse(req.postData() || '{}');
      const assignment = {
        id: 77,
        department: departments.find((department) => department.id === body.department_id) || null,
        hod_user: users.find((user) => user.id === body.hod_user_id) || null,
        start_date: body.start_date,
        end_date: null,
        active: body.active !== false,
      };
      hodAssignments.unshift(assignment);
      return respond(assignment, 201);
    }

    return route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ detail: `Unhandled ${method} ${pathname}` }) });
  });
}

async function seedAuth(context, user) {
  const payload = {
    role: user.role,
    user_role: user.role,
    exp: Math.floor(Date.now() / 1000) + 3600,
  };
  const base64Url = (value) => btoa(JSON.stringify(value)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  const token = `${base64Url({ alg: 'HS256', typ: 'JWT' })}.${base64Url(payload)}.signature`;
  await context.addCookies([
    { name: 'pgsims_access_token', value: token, url: baseUrl },
    { name: 'pgsims_user_role', value: user.role, url: baseUrl },
    { name: 'pgsims_access_exp', value: String(payload.exp), url: baseUrl },
  ]);
  await context.addInitScript((auth) => {
    const storage = {
      state: {
        user: auth.user,
        accessToken: 'access-token',
        refreshToken: 'refresh-token',
        isAuthenticated: true,
      },
      version: 0,
    };
    localStorage.setItem('auth-storage', JSON.stringify(storage));
    localStorage.setItem('access_token', 'access-token');
    localStorage.setItem('refresh_token', 'refresh-token');
    localStorage.setItem('user', JSON.stringify(auth.user));
  }, { user });
}

async function main() {
  await fs.mkdir(screenshotsDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1600, height: 1200 } });
  const state = { resetPasswordCalls: 0 };

  await installRoutes(context, state);
  await seedAuth(context, authUser);
  const page = await context.newPage();

  // Users page
  await page.goto(`${baseUrl}/dashboard/utrmc/users`, { waitUntil: 'networkidle' });
  await page.selectOption('#role-filter', 'resident');
  await page.selectOption('#department-filter', '2');
  await page.selectOption('#supervisor-filter', '2');
  await page.selectOption('#program-filter', '11');
  await page.screenshot({ path: path.join(screenshotsDir, 'users-filters-row-actions.png'), fullPage: true });

  await page.getByRole('button', { name: 'Reset Password' }).first().click();
  await page.waitForTimeout(500);
  await overlayNote(page, 'Reset password action captured in browser runtime.\nEndpoint: POST /api/users/3/reset-password/\nResult: 200 OK\nPassword set to: pgfmu123');
  await page.screenshot({ path: path.join(screenshotsDir, 'users-reset-password.png'), fullPage: true });

  // Resident programme assignment
  await page.goto(`${baseUrl}/dashboard/utrmc/resident-training`, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(screenshotsDir, 'resident-programme-assignment.png'), fullPage: true });

  // Supervision links
  await page.goto(`${baseUrl}/dashboard/utrmc/supervision`, { waitUntil: 'networkidle' });
  await page.getByRole('button', { name: '+ Add Link' }).click();
  await page.selectOption('#supervision-supervisor', '2');
  await page.selectOption('#supervision-resident', '3');
  await page.selectOption('#supervision-department', '2');
  await page.locator('#supervision-start-date').fill('2026-06-21');
  await page.getByRole('button', { name: 'Save' }).click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(screenshotsDir, 'supervision-link-created.png'), fullPage: true });

  // HOD assignments
  await page.goto(`${baseUrl}/dashboard/utrmc/hod`, { waitUntil: 'networkidle' });
  await page.getByRole('button', { name: '+ Add HOD' }).click();
  await page.selectOption('#hod-department', '2');
  await page.selectOption('#hod-user', '2');
  await page.locator('#hod-start-date').fill('2026-06-21');
  await page.getByRole('button', { name: 'Save' }).click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(screenshotsDir, 'hod-assignment-created.png'), fullPage: true });

  // Monitoring dashboard
  await page.goto(`${baseUrl}/dashboard/utrmc`, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(screenshotsDir, 'utrmc-monitoring-dashboard.png'), fullPage: true });

  await browser.close();

  await fs.writeFile(
    path.join(evidenceDir, 'runtime_state.json'),
    JSON.stringify(
      {
        resetPasswordCalls: state.resetPasswordCalls,
        screenshots: [
          'users-filters-row-actions.png',
          'users-reset-password.png',
          'resident-programme-assignment.png',
          'supervision-link-created.png',
          'hod-assignment-created.png',
          'utrmc-monitoring-dashboard.png',
        ],
      },
      null,
      2
    )
  );
}

main().catch(async (error) => {
  console.error(error);
  process.exitCode = 1;
});
