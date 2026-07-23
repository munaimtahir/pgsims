'use client';

import { useState } from 'react';
import ImportExportPanel from '@/components/ui/ImportExportPanel';
import FlexibleMappingImport from './FlexibleMappingImport';

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
    title: 'Training Programs',
    entity: 'training-programs',
    exportResource: 'training_programs',
    description: 'Load the training programme list (e.g. MS Medicine, FCPS Surgery) that residents are registered against.',
    expectedColumns: [
      { name: 'program_code', required: true, note: 'Stable programme code used by later imports.' },
      { name: 'program_name', required: true },
      { name: 'duration_months', required: true, note: 'Total programme duration in months.' },
      { name: 'active' },
    ],
  },
  {
    step: 'Step 5',
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
    step: 'Step 6',
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
    step: 'Step 7',
    title: 'Supervision Assignments',
    entity: 'supervision-links',
    exportResource: 'supervision-links',
    description: 'Apply resident-to-supervisor assignments after both user datasets are loaded.',
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
    step: 'Step 8',
    title: 'Rotation / Placement Assignments',
    entity: 'rotation-assignments',
    exportResource: 'rotation-assignments',
    description: 'Load rotation placements linking residents to a hospital-department for a date range. Apply last, after residents and the matrix are both loaded.',
    expectedColumns: [
      { name: 'resident_email', required: true },
      { name: 'hospital_code', required: true },
      { name: 'department_code', required: true },
      { name: 'start_date', required: true },
      { name: 'end_date', required: true },
      { name: 'status', note: 'Defaults to DRAFT.' },
      { name: 'notes' },
    ],
  },
];

export default function BulkSetupWorkspace() {
  const [importMode, setImportMode] = useState<'standard' | 'flexible'>('standard');

  return (
    <section className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Bulk Setup & Import/Export</h2>
        <p className="mt-1 text-sm text-gray-500">
          Use the template workflow or configure flexible custom mappings to load trainee rosters, supervisor datasets, placements and matrix connections.
        </p>
      </div>

      {/* Mode selection tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setImportMode('standard')}
          className={`py-2.5 px-4 text-sm font-semibold border-b-2 transition-all ${
            importMode === 'standard'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Use Standard Template (Recommended)
        </button>
        <button
          onClick={() => setImportMode('flexible')}
          className={`py-2.5 px-4 text-sm font-semibold border-b-2 transition-all ${
            importMode === 'flexible'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Upload Custom File & Map Columns
        </button>
      </div>

      {importMode === 'standard' ? (
        <div className="space-y-6">
          <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
            Prerequisite order matters: hospitals, departments, matrix, faculty/supervisors, residents, then supervision links.
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
        </div>
      ) : (
        <div className="space-y-6">
          <div className="rounded-xl border border-indigo-100 bg-indigo-50/45 p-4 text-sm text-indigo-900">
            <span className="font-semibold block mb-0.5">Flexible Column Mapping Import</span>
            Upload a CSV or Excel file from any custom source. You will match your headers to the required PGSIMS target fields, preview in-memory validation, save your preset, and apply final database loads.
          </div>

          <FlexibleMappingImport />
        </div>
      )}
    </section>
  );
}
