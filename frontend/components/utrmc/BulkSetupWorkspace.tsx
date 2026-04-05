'use client';

import ImportExportPanel from '@/components/ui/ImportExportPanel';

const PANELS = [
  {
    step: 'Step 1',
    title: 'Hospitals',
    entity: 'hospitals',
    exportResource: 'hospitals',
    description: 'Load the canonical hospital list first. Later imports reference hospital_code values from this dataset.',
    expectedColumns: [
      { name: 'hospital_code', required: true, note: 'Stable hospital code used by later imports.' },
      { name: 'hospital_name', required: true },
      { name: 'address' },
      { name: 'phone' },
      { name: 'email' },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 2',
    title: 'Departments',
    entity: 'departments',
    exportResource: 'departments',
    description: 'Load the single canonical department list. Do not create duplicate department concepts outside this import.',
    expectedColumns: [
      { name: 'department_code', required: true, note: 'Canonical department code.' },
      { name: 'department_name', required: true },
      { name: 'description' },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 3',
    title: 'Hospital-Department Matrix',
    entity: 'matrix',
    exportResource: 'matrix',
    description: 'Link hospitals to the departments they host. User site assignments depend on this matrix being loaded first.',
    expectedColumns: [
      { name: 'hospital_code', required: true },
      { name: 'department_code', required: true },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 4',
    title: 'Faculty & Supervisors',
    entity: 'faculty-supervisors',
    exportResource: 'faculty-supervisors',
    description: 'Create faculty/supervisor accounts and their primary department membership. Include hospital_code only after the matrix exists.',
    expectedColumns: [
      { name: 'email', required: true },
      { name: 'full_name', required: true },
      { name: 'phone_number' },
      { name: 'role', required: true, note: 'Must be faculty or supervisor.' },
      { name: 'specialty' },
      { name: 'department_code' },
      { name: 'hospital_code', note: 'Optional but requires the matrix row to exist.' },
      { name: 'designation' },
      { name: 'registration_number' },
      { name: 'username' },
      { name: 'password', note: 'Optional. Leave blank to generate a temporary password.' },
      { name: 'active' },
      { name: 'start_date' },
    ],
  },
  {
    step: 'Step 5',
    title: 'Residents',
    entity: 'residents',
    exportResource: 'residents',
    description: 'Create resident/PG accounts, resident profiles, and optional home site setup. Include department_code and hospital_code to fully wire roster and site data.',
    expectedColumns: [
      { name: 'email', required: true },
      { name: 'full_name', required: true },
      { name: 'phone_number' },
      { name: 'role', note: 'Optional. Defaults to resident; accepts resident or pg.' },
      { name: 'specialty', required: true },
      { name: 'year', required: true },
      { name: 'pgr_id' },
      { name: 'training_start', required: true },
      { name: 'training_end' },
      { name: 'training_level' },
      { name: 'department_code' },
      { name: 'hospital_code', note: 'Optional but requires the matrix row to exist.' },
      { name: 'supervisor_email' },
      { name: 'username' },
      { name: 'password', note: 'Optional. Leave blank to generate a temporary password.' },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 6',
    title: 'Supervision Links',
    entity: 'supervision-links',
    exportResource: 'supervision-links',
    description: 'Apply resident-to-faculty/supervisor links after both user datasets are loaded.',
    expectedColumns: [
      { name: 'supervisor_email', required: true },
      { name: 'resident_email', required: true },
      { name: 'department_code' },
      { name: 'start_date', required: true },
      { name: 'end_date' },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 7',
    title: 'HOD Assignments',
    entity: 'hod-assignments',
    exportResource: 'hod-assignments',
    description: 'Assign the active HOD per department after faculty/supervisor accounts and departments exist.',
    expectedColumns: [
      { name: 'department_code', required: true },
      { name: 'hod_email', required: true },
      { name: 'start_date', required: true },
      { name: 'end_date' },
      { name: 'active' },
    ],
  },
];

export default function BulkSetupWorkspace() {
  return (
    <section className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Bulk Setup & Import/Export</h2>
        <p className="mt-1 text-sm text-gray-500">
          Use the prerequisite order below. Dry run first, then apply, then export the resulting truth if you need a reconciliation copy.
        </p>
      </div>

      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
        Prerequisite order matters: hospitals, departments, matrix, faculty/supervisors, residents, supervision links, then HOD assignments.
      </div>

      <div className="space-y-6">
        {PANELS.map((panel) => (
          <div key={panel.entity} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <div className="mb-4 flex items-center gap-3">
              <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-indigo-700">
                {panel.step}
              </span>
              <h3 className="text-lg font-semibold text-gray-900">{panel.title}</h3>
            </div>

            <ImportExportPanel
              entity={panel.entity}
              label={panel.title}
              exportResource={panel.exportResource}
              templateResource={panel.entity}
              expectedColumns={panel.expectedColumns}
              description={panel.description}
            />
          </div>
        ))}
      </div>
    </section>
  );
}
