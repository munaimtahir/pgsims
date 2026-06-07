'use client';

import React, { useState, useEffect, useRef } from 'react';
import apiClient from '@/lib/api/client';
import ErrorBanner from '@/components/ui/ErrorBanner';
import SuccessBanner from '@/components/ui/SuccessBanner';
import { downloadFile } from '@/lib/utils';
import { Upload, FileSpreadsheet, Map, CheckCircle2, AlertTriangle, Play, Save, Trash2, ArrowRight, ArrowLeft } from 'lucide-react';

interface SchemaField {
  name: string;
  label: string;
  required: boolean;
  type: string;
  choices?: string[];
}

interface SchemaDefinition {
  label: string;
  fields: SchemaField[];
}

interface Preset {
  id: number;
  name: string;
  entity: string;
  mapping: Record<string, string>;
  created_at: string;
  last_used_at: string | null;
}

interface ValidationResponse {
  ready: boolean;
  missing_required: string[];
  duplicate_mappings: Record<string, string[]>;
  required_fields: string[];
  optional_fields: string[];
}

interface DryRunResponse {
  success_count: number;
  failure_count: number;
  dry_run: boolean;
  rows: Array<Record<string, string> & { _row_number: number }>;
  details?: {
    successes?: Array<{ row: number; email?: string; [key: string]: unknown }>;
    failures?: Array<{ row: number; error: string }>;
  };
}

export default function FlexibleMappingImport() {
  // Stepper state: 1 = Upload, 2 = Mapping, 3 = Dry Run / Preview
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Phase 4 & 5 state: File, Target Schema, Detected Headers
  const [entity, setEntity] = useState<string>('residents');
  const [file, setFile] = useState<File | null>(null);
  const [schemas, setSchemas] = useState<Record<string, SchemaDefinition>>({});
  const [headers, setHeaders] = useState<string[]>([]);
  const [sampleRows, setSampleRows] = useState<Array<Record<string, string>>>([]);
  const [totalRows, setTotalRows] = useState<number>(0);
  const [sheets, setSheets] = useState<string[]>([]);
  const [sheetName, setSheetName] = useState<string>('');
  
  // Phase 6 & 7 state: Column Mappings
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [presets, setPresets] = useState<Preset[]>([]);
  const [selectedPresetId, setSelectedPresetId] = useState<string>('');
  const [newPresetName, setNewPresetName] = useState<string>('');
  const [isSavingPreset, setIsSavingPreset] = useState(false);
  const [mappingValidation, setMappingValidation] = useState<ValidationResponse | null>(null);

  // Phase 9 & 10 state: Dry-run and Row Previews
  const [dryRunResult, setDryRunResult] = useState<DryRunResponse | null>(null);
  const [importMode, setImportMode] = useState<'strict' | 'partial'>('strict');

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load schemas and presets on mount
  useEffect(() => {
    fetchSchemas();
    fetchPresets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Re-fetch presets or validate mapping whenever entity changes
  useEffect(() => {
    if (entity) {
      fetchPresets();
      setMapping({});
      setHeaders([]);
      setSampleRows([]);
      setTotalRows(0);
      setSheets([]);
      setSheetName('');
      setDryRunResult(null);
      setMappingValidation(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      setFile(null);
      setStep(1);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entity]);

  // Run validation whenever mapping dictionary changes
  useEffect(() => {
    if (Object.keys(mapping).length > 0 && entity) {
      validateMappingState();
    } else {
      setMappingValidation(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mapping]);

  const fetchSchemas = async () => {
    try {
      const response = await apiClient.get<Record<string, SchemaDefinition>>('/api/bulk/flexible/schemas/');
      setSchemas(response.data);
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to load import schemas.');
    }
  };

  const fetchPresets = async () => {
    try {
      const response = await apiClient.get<{ results: Preset[] }>(`/api/bulk/flexible/presets/?entity=${entity}`);
      setPresets(response.data.results);
    } catch (err: unknown) {
      console.error('Failed to load presets', err);
    }
  };

  const handleFileUpload = async (uploadedFile: File, activeSheetName?: string) => {
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      if (activeSheetName) {
        formData.append('sheet_name', activeSheetName);
      }

      const response = await apiClient.post<{
        headers: string[];
        sample_rows: Array<Record<string, string>>;
        total_rows: number;
        sheets: string[];
      }>('/api/bulk/flexible/detect-headers/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setFile(uploadedFile);
      setHeaders(response.data.headers);
      setSampleRows(response.data.sample_rows);
      setTotalRows(response.data.total_rows);
      setSheets(response.data.sheets || []);
      if (response.data.sheets && response.data.sheets.length > 0 && !activeSheetName) {
        setSheetName(response.data.sheets[0]);
      }

      // Phase 7: Auto-mapping suggestions using normalized match rules
      const currentSchema = schemas[entity];
      if (currentSchema) {
        const autoMapping: Record<string, string> = {};
        
        currentSchema.fields.forEach((field) => {
          const suggestions = getAutoSuggestionsForField(field.name);
          const matchedHeader = response.data.headers.find((header) => {
            const normalizedHeader = header.toLowerCase().replace(/[^a-z0-9]/g, '');
            return suggestions.includes(normalizedHeader);
          });
          
          if (matchedHeader) {
            autoMapping[field.name] = matchedHeader;
          } else {
            autoMapping[field.name] = '';
          }
        });
        setMapping(autoMapping);
      }

      setSuccess(`File "${uploadedFile.name}" successfully parsed. Detected ${response.data.headers.length} columns and ${response.data.total_rows} rows.`);
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to analyze uploaded file.');
      setFile(null);
      setHeaders([]);
      setSampleRows([]);
      setTotalRows(0);
    } finally {
      setLoading(false);
    }
  };

  const getAutoSuggestionsForField = (fieldName: string): string[] => {
    const mappingRules: Record<string, string[]> = {
      email: ['email', 'emailaddress', 'emailid', 'mail', 'residentemail', 'supervisoremail', 'hodemail', 'customemail'],
      full_name: ['name', 'fullname', 'residentname', 'supervisorname', 'supervisor', 'facultyname', 'faculty', 'customname'],
      phone_number: ['phone', 'phonenumber', 'mobile', 'mobilecode', 'contact', 'cell', 'contactnumber'],
      role: ['role', 'designation', 'userrole'],
      specialty: ['specialty', 'speciality', 'deptspecialty', 'specialtyarea'],
      year: ['year', 'trainingyear', 'yearoftraining'],
      pgr_id: ['pgrid', 'enrollmentno', 'registrationno', 'pmdcno', 'pmdc', 'registrationnumber'],
      training_start: ['trainingstart', 'trainingstartdate', 'startdate', 'joiningdate'],
      training_end: ['trainingend', 'trainingenddate', 'enddate'],
      training_level: ['traininglevel', 'level'],
      department_code: ['departmentcode', 'department', 'dept', 'specialtycode', 'deptcode'],
      hospital_code: ['hospitalcode', 'hospital', 'instcode', 'traininghospital', 'institute'],
      supervisor_email: ['supervisoremail', 'supervisor', 'facultysupervisoremail'],
      resident_email: ['residentemail', 'resident', 'traineeemail'],
      hod_email: ['hodemail', 'hod', 'headofdepartmentemail'],
      start_date: ['startdate', 'joiningdate', 'fromdate'],
      end_date: ['enddate', 'todate'],
      status: ['status', 'state'],
      notes: ['notes', 'remarks', 'comment', 'description'],
      hospital_name: ['hospitalname', 'name', 'instname'],
      address: ['address', 'location'],
      phone: ['phone', 'telephone'],
      department_name: ['departmentname', 'deptname'],
      description: ['description', 'desc'],
      active: ['active', 'status', 'isenabled'],
      password: ['password', 'pass', 'userpassword', 'pwd', 'passcode']
    };
    return mappingRules[fieldName] || [fieldName.toLowerCase().replace(/[^a-z0-9]/g, '')];
  };

  const validateMappingState = async () => {
    try {
      const response = await apiClient.post<ValidationResponse>('/api/bulk/flexible/validate-mapping/', {
        entity,
        mapping,
      });
      setMappingValidation(response.data);
    } catch (err: unknown) {
      console.error('Mapping validation error', err);
    }
  };

  const handleApplyPreset = (preset: Preset) => {
    const loadedMapping = { ...mapping };
    // Only map headers that exist in current file
    Object.keys(preset.mapping).forEach((field) => {
      const val = preset.mapping[field];
      if (headers.includes(val)) {
        loadedMapping[field] = val;
      } else {
        loadedMapping[field] = '';
      }
    });
    setMapping(loadedMapping);
    setSuccess(`Loaded preset: ${preset.name}`);
  };

  const handleSavePreset = async () => {
    if (!newPresetName.trim()) {
      setError('Please provide a name for the mapping preset.');
      return;
    }
    setError(null);
    setIsSavingPreset(true);
    try {
      const response = await apiClient.post<Preset>('/api/bulk/flexible/presets/', {
        name: newPresetName,
        entity,
        mapping,
      });
      setPresets([response.data, ...presets]);
      setSelectedPresetId(response.data.id.toString());
      setNewPresetName('');
      setSuccess(`Preset "${response.data.name}" saved successfully.`);
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to save preset.');
    } finally {
      setIsSavingPreset(false);
    }
  };

  const handleDeletePreset = async (presetId: number) => {
    if (!confirm('Are you sure you want to delete this preset?')) return;
    setError(null);
    try {
      await apiClient.delete(`/api/bulk/flexible/presets/${presetId}/`);
      setPresets(presets.filter((p) => p.id !== presetId));
      if (selectedPresetId === presetId.toString()) {
        setSelectedPresetId('');
      }
      setSuccess('Preset deleted successfully.');
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to delete preset.');
    }
  };

  const runDryRun = async () => {
    if (!file) return;
    setError(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('entity', entity);
      formData.append('mapping', JSON.stringify(mapping));
      if (sheetName) {
        formData.append('sheet_name', sheetName);
      }

      const response = await apiClient.post<DryRunResponse>('/api/bulk/flexible/dry-run/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setDryRunResult(response.data);
      const errors = response.data.failure_count;
      setSuccess(
        `Dry Run Complete: ${response.data.success_count} rows valid, ${errors} rows invalid/blocked.`
      );
      setStep(3);
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to perform dry-run validation.');
    } finally {
      setLoading(false);
    }
  };

  const runApplyImport = async () => {
    if (!file) return;
    if (!confirm(`Are you sure you want to run final import in ${importMode.toUpperCase()} mode? This writes directly to the database.`)) {
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('entity', entity);
      formData.append('mapping', JSON.stringify(mapping));
      formData.append('import_mode', importMode);
      if (sheetName) {
        formData.append('sheet_name', sheetName);
      }
      if (selectedPresetId) {
        formData.append('preset_id', selectedPresetId);
      }

      const response = await apiClient.post<{ success_count: number; failure_count: number }>('/api/bulk/flexible/apply/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setSuccess(`Import succeeded! Successfully imported ${response.data.success_count} records. Failed/Skipped: ${response.data.failure_count}.`);
      setDryRunResult(null);
      setFile(null);
      setStep(1);
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { detail?: string } } };
      setError(apiErr?.response?.data?.detail || 'Failed to execute import.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadTransformed = () => {
    if (!dryRunResult?.rows) return;
    
    const fields = schemas[entity].fields.map((f) => f.name);
    const csvContent = [
      fields.join(','),
      ...dryRunResult.rows.map((row) => 
        fields.map((field) => {
          const val = row[field] || '';
          return `"${val.replace(/"/g, '""')}"`;
        }).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    downloadFile(blob, `${entity}_transformed_preview.csv`);
  };

  const handleDownloadErrorReport = () => {
    if (!dryRunResult?.details?.failures) return;
    
    const csvContent = [
      'Row Number,Error Description',
      ...dryRunResult.details.failures.map((f) => `${f.row},"${f.error.replace(/"/g, '""')}"`)
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    downloadFile(blob, `${entity}_import_error_report.csv`);
  };

  // Safe checks
  const currentSchema = schemas[entity];
  const isMappingReady = mappingValidation?.ready || false;

  return (
    <div className="space-y-6">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
      {success && <SuccessBanner message={success} onDismiss={() => setSuccess(null)} />}

      <div className="rounded-2xl border border-gray-200 bg-white shadow-sm overflow-hidden">
        {/* Stepper Header */}
        <div className="flex border-b border-gray-200 bg-gray-50/50 p-4">
          {[
            { id: 1, label: 'Upload & Parse', icon: Upload },
            { id: 2, label: 'Column Mapping', icon: Map },
            { id: 3, label: 'Dry-Run & Preview', icon: Play },
          ].map((s) => {
            const Icon = s.icon;
            const active = step === s.id;
            const done = step > s.id;
            return (
              <div
                key={s.id}
                className={`flex-1 flex items-center justify-center gap-2 border-b-2 py-2 px-1 text-sm font-medium transition-all ${
                  active
                    ? 'border-indigo-600 text-indigo-600'
                    : done
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-400'
                }`}
              >
                <span className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold ${
                  active
                    ? 'bg-indigo-600 text-white'
                    : done
                    ? 'bg-emerald-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}>
                  {s.id}
                </span>
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{s.label}</span>
              </div>
            );
          })}
        </div>

        {/* Step Content */}
        <div className="p-6">
          {step === 1 && (
            <div className="space-y-6">
              {/* Select target entity */}
              <div className="max-w-md">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Select Import Target
                </label>
                <select
                  data-testid="select-import-target"
                  value={entity}
                  onChange={(e) => setEntity(e.target.value)}
                  className="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none"
                >
                  {Object.keys(schemas).map((key) => (
                    <option key={key} value={key}>
                      {schemas[key].label}
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-xs text-gray-500">
                  Select the database records you want to load using the custom columns.
                </p>
              </div>

              {/* Upload Dropzone */}
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center bg-gray-50 hover:bg-gray-100/70 transition cursor-pointer relative">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) handleFileUpload(f);
                  }}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <div className="flex flex-col items-center justify-center space-y-3">
                  <div className="rounded-full bg-indigo-50 p-3">
                    <FileSpreadsheet className="h-8 w-8 text-indigo-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-800">
                      {file ? `Selected file: ${file.name}` : 'Click to upload or drag & drop CSV/Excel file'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Supports CSV, XLSX, XLS files up to 10MB.
                    </p>
                  </div>
                </div>
              </div>

              {/* Excel Sheets selection */}
              {sheets.length > 1 && (
                <div className="max-w-xs">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Select Sheet (Multi-sheet Excel)
                  </label>
                  <select
                    value={sheetName}
                    onChange={(e) => {
                      setSheetName(e.target.value);
                      if (file) handleFileUpload(file, e.target.value);
                    }}
                    className="block w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm"
                  >
                    {sheets.map((sheet) => (
                      <option key={sheet} value={sheet}>
                        {sheet}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* File details overview */}
              {file && headers.length > 0 && (
                <div className="rounded-xl border border-gray-200 bg-white p-4 space-y-3">
                  <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                    <h4 className="text-sm font-semibold text-gray-900">File Analysis</h4>
                    <span className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-semibold text-indigo-700">
                      Parsed successfully
                    </span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="block text-xs text-gray-500 font-medium uppercase">File Name</span>
                      <span className="font-semibold text-gray-800 block truncate">{file.name}</span>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500 font-medium uppercase">Total Rows</span>
                      <span className="font-semibold text-gray-800">{totalRows}</span>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500 font-medium uppercase">Columns Found</span>
                      <span className="font-semibold text-gray-800">{headers.length}</span>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500 font-medium uppercase">File Type</span>
                      <span className="font-semibold text-gray-800 uppercase">{file.name.split('.').pop()}</span>
                    </div>
                  </div>

                  {/* Sample rows preview */}
                  <div className="mt-4">
                    <span className="block text-xs text-gray-500 font-medium uppercase mb-2">Sample File Rows</span>
                    <div className="overflow-x-auto max-h-36 border border-gray-100 rounded-lg">
                      <table className="min-w-full text-left text-xs">
                        <thead className="bg-gray-50 text-gray-600 uppercase border-b border-gray-100">
                          <tr>
                            {headers.slice(0, 5).map((h) => (
                              <th key={h} className="px-3 py-2 font-semibold">{h}</th>
                            ))}
                            {headers.length > 5 && <th className="px-3 py-2 font-semibold">...</th>}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100 text-gray-800">
                          {sampleRows.slice(0, 3).map((row, rIdx) => (
                            <tr key={rIdx}>
                              {headers.slice(0, 5).map((h) => (
                                <td key={h} className="px-3 py-1.5 truncate max-w-xs">{row[h] || '-'}</td>
                              ))}
                              {headers.length > 5 && <td className="px-3 py-1.5 text-gray-400">...</td>}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* Action */}
              <div className="flex justify-end pt-2">
                <button
                  disabled={loading || !file || headers.length === 0}
                  onClick={() => setStep(2)}
                  className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50 transition shadow-sm"
                >
                  Continue to Mapping
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {step === 2 && currentSchema && (
            <div className="space-y-6">
              {/* Presets loader/saver */}
              <div className="flex flex-wrap items-end gap-4 border-b border-gray-100 pb-4">
                <div className="max-w-xs flex-1">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                    Load Existing Preset
                  </label>
                  <div className="flex gap-2">
                    <select
                      value={selectedPresetId}
                      onChange={(e) => {
                        setSelectedPresetId(e.target.value);
                        const preset = presets.find((p) => p.id.toString() === e.target.value);
                        if (preset) handleApplyPreset(preset);
                      }}
                      className="block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none"
                    >
                      <option value="">-- Choose Mapping Preset --</option>
                      {presets.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name}
                        </option>
                      ))}
                    </select>
                    {selectedPresetId && (
                      <button
                        type="button"
                        onClick={() => handleDeletePreset(parseInt(selectedPresetId))}
                        className="rounded-lg border border-red-200 p-2 text-red-600 hover:bg-red-50"
                        title="Delete Preset"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>

                <div className="max-w-xs flex-1">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
                    Save Mapping as Preset
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Preset name (e.g. Google Form Residents)"
                      value={newPresetName}
                      onChange={(e) => setNewPresetName(e.target.value)}
                      className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none"
                    />
                    <button
                      type="button"
                      disabled={isSavingPreset || !newPresetName.trim()}
                      onClick={handleSavePreset}
                      className="flex items-center gap-1.5 rounded-lg bg-indigo-50 px-3 py-2 text-sm font-semibold text-indigo-700 hover:bg-indigo-100 disabled:opacity-50 transition"
                    >
                      <Save className="h-4 w-4" />
                      Save
                    </button>
                  </div>
                </div>
              </div>

              {/* Mappings Table */}
              <div className="overflow-x-auto rounded-xl border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200 text-left text-sm">
                  <thead className="bg-gray-50 text-xs font-semibold uppercase text-gray-500">
                    <tr>
                      <th className="px-4 py-3">PGSIMS Field</th>
                      <th className="px-4 py-3">Required</th>
                      <th className="px-4 py-3">Source Column from Uploaded File</th>
                      <th className="px-4 py-3">Sample Value</th>
                      <th className="px-4 py-3">Expected Format / Guide</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 bg-white text-gray-700">
                    {currentSchema.fields.map((field) => {
                      const selectedVal = mapping[field.name] || '';
                      // Find sample value
                      const sampleRow = sampleRows[0] || {};
                      const sampleVal = selectedVal ? sampleRow[selectedVal] : '';
                      const autoMapped = getAutoSuggestionsForField(field.name).includes(
                        selectedVal.toLowerCase().replace(/[^a-z0-9]/g, '')
                      );

                      return (
                        <tr key={field.name} className="hover:bg-gray-50/50">
                          <td className="px-4 py-3.5">
                            <span className="font-semibold text-gray-900">{field.label}</span>
                            <span className="block text-xs text-gray-500 mt-0.5">{field.name}</span>
                          </td>
                          <td className="px-4 py-3.5">
                            {field.required ? (
                              <span className="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
                                Required
                              </span>
                            ) : (
                              <span className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">
                                Optional
                              </span>
                            )}
                          </td>
                          <td className="px-4 py-3.5">
                            <select
                              data-testid={`select-mapping-${field.name}`}
                              value={selectedVal}
                              onChange={(e) => {
                                setMapping({
                                  ...mapping,
                                  [field.name]: e.target.value,
                                });
                              }}
                              className={`block w-full max-w-xs rounded-lg border px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none ${
                                selectedVal
                                  ? autoMapped
                                    ? 'border-emerald-200 bg-emerald-50/30'
                                    : 'border-indigo-200 bg-indigo-50/20'
                                  : field.required
                                  ? 'border-amber-300 bg-amber-50/30'
                                  : 'border-gray-300'
                              }`}
                            >
                              <option value="">-- Choose Column (Unmapped) --</option>
                              {headers.map((h) => (
                                <option key={h} value={h}>
                                  {h}
                                </option>
                              ))}
                            </select>
                          </td>
                          <td className="px-4 py-3.5 max-w-xs truncate font-mono text-xs text-gray-600">
                            {sampleVal !== undefined && sampleVal !== '' ? sampleVal : <span className="text-gray-400 font-normal italic">None</span>}
                          </td>
                          <td className="px-4 py-3.5 text-xs text-gray-500">
                            <span className="block font-medium text-gray-600 capitalize">Type: {field.type}</span>
                            {field.choices && (
                              <span className="block truncate max-w-xs mt-0.5 text-gray-400">
                                Choices: {field.choices.join(', ')}
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Mapping validation summary */}
              {mappingValidation && (
                <div className={`rounded-xl border p-4 text-sm ${isMappingReady ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-amber-200 bg-amber-50 text-amber-800'}`}>
                  <div className="flex items-center gap-2 font-semibold">
                    {isMappingReady ? (
                      <>
                        <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                        Mapping Valid & Ready to Preview
                      </>
                    ) : (
                      <>
                        <AlertTriangle className="h-5 w-5 text-amber-600" />
                        Incomplete Mapping Setup
                      </>
                    )}
                  </div>
                  <div className="mt-2 space-y-1 text-xs">
                    {mappingValidation?.missing_required && mappingValidation.missing_required.length > 0 && (
                      <p>
                        <span className="font-semibold">Missing required fields:</span>{' '}
                        {mappingValidation.missing_required.map((f) => currentSchema.fields.find((field) => field.name === f)?.label || f).join(', ')}
                      </p>
                    )}
                    {mappingValidation?.duplicate_mappings && Object.keys(mappingValidation.duplicate_mappings).length > 0 && (
                      <p>
                        <span className="font-semibold text-red-600">Duplicate column bindings:</span>{' '}
                        {Object.entries(mappingValidation.duplicate_mappings).map(([col, fields]) => `"${col}" mapped to multiple fields (${fields.join(', ')})`).join('; ')}
                      </p>
                    )}
                    {!isMappingReady && (
                      <p className="mt-1 text-[11px] text-amber-700/80">
                        Please map all required fields and resolve duplicate mappings before executing dry run.
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Action buttons */}
              <div className="flex justify-between pt-2">
                <button
                  onClick={() => setStep(1)}
                  className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back to Upload
                </button>

                <button
                  disabled={loading || !isMappingReady}
                  onClick={runDryRun}
                  className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50 transition shadow-sm"
                >
                  {loading ? 'Analyzing...' : 'Execute Dry-Run & Preview'}
                  <Play className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {step === 3 && dryRunResult && (
            <div className="space-y-6">
              {/* Validation results summary cards */}
              <div>
                <h4 className="text-sm font-semibold text-gray-900 mb-3">Dry-Run Validation Summary</h4>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="rounded-xl border border-gray-200 bg-white p-4 text-center">
                    <span className="block text-xs font-semibold text-gray-500 uppercase">Total Uploaded</span>
                    <span className="block text-2xl font-bold text-gray-800 mt-1">{totalRows}</span>
                  </div>
                  <div className="rounded-xl border border-emerald-100 bg-emerald-50/20 p-4 text-center">
                    <span className="block text-xs font-semibold text-emerald-600 uppercase">Valid Rows</span>
                    <span className="block text-2xl font-bold text-emerald-700 mt-1">{dryRunResult.success_count}</span>
                  </div>
                  <div className="rounded-xl border border-red-100 bg-red-50/20 p-4 text-center">
                    <span className="block text-xs font-semibold text-red-500 uppercase">Errors/Failures</span>
                    <span className="block text-2xl font-bold text-red-600 mt-1">{dryRunResult.failure_count}</span>
                  </div>
                  <div className="rounded-xl border border-gray-200 bg-white p-4 text-center">
                    <span className="block text-xs font-semibold text-gray-500 uppercase">Status</span>
                    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold mt-2 ${
                      dryRunResult.failure_count === 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {dryRunResult.failure_count === 0 ? 'Fully Valid' : 'Contains Errors'}
                    </span>
                  </div>
                  <div className="rounded-xl border border-gray-200 bg-white p-4 text-center col-span-2 md:col-span-1">
                    <span className="block text-xs font-semibold text-gray-500 uppercase">Verification</span>
                    <span className="block text-sm font-semibold text-gray-700 mt-2">Dry-Run Only</span>
                    <span className="block text-[10px] text-gray-400">No database edits made</span>
                  </div>
                </div>
              </div>

              {/* Transformed Preview Grid */}
              <div>
                <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
                  <h4 className="text-sm font-semibold text-gray-900">Transformed Preview Rows</h4>
                  <div className="flex gap-2">
                    <button
                      onClick={handleDownloadTransformed}
                      className="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-gray-700 hover:bg-gray-50"
                    >
                      Download Transformed CSV
                    </button>
                    {dryRunResult.failure_count > 0 && (
                      <button
                        onClick={handleDownloadErrorReport}
                        className="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-700 hover:bg-red-100"
                      >
                        Download Error Report CSV
                      </button>
                    )}
                  </div>
                </div>

                <div className="overflow-x-auto max-h-72 border border-gray-200 rounded-xl">
                  <table className="min-w-full divide-y divide-gray-200 text-left text-xs">
                    <thead className="bg-gray-50 text-gray-600 font-semibold uppercase sticky top-0 border-b border-gray-200">
                      <tr>
                        <th className="px-3 py-2 text-center w-16">Row</th>
                        <th className="px-3 py-2">Validation Status</th>
                        {currentSchema.fields.slice(0, 6).map((f) => (
                          <th key={f.name} className="px-3 py-2">{f.label}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 bg-white text-gray-800">
                      {dryRunResult.rows.map((row, idx) => {
                        const rowNum = row._row_number;
                        const errorDetail = dryRunResult.details?.failures?.find((f) => f.row === rowNum);
                        const isValid = !errorDetail;

                        return (
                          <React.Fragment key={idx}>
                            <tr className={isValid ? 'hover:bg-gray-50/50' : 'bg-red-50/20 hover:bg-red-50/30'}>
                              <td className="px-3 py-2.5 text-center font-medium text-gray-500">{rowNum}</td>
                              <td className="px-3 py-2.5">
                                {isValid ? (
                                  <span className="inline-flex items-center gap-1 text-emerald-700 font-semibold">
                                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                                    Valid
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center gap-1 text-red-700 font-semibold">
                                    <AlertTriangle className="h-3.5 w-3.5 text-red-500" />
                                    Error
                                  </span>
                                )}
                              </td>
                              {currentSchema.fields.slice(0, 6).map((f) => (
                                <td key={f.name} className="px-3 py-2.5 truncate max-w-xs">{row[f.name] || '-'}</td>
                              ))}
                            </tr>
                            {!isValid && (
                              <tr className="bg-red-50/40">
                                <td colSpan={2 + Math.min(6, currentSchema.fields.length)} className="px-3 py-1.5 text-[11px] text-red-600 font-medium border-b border-red-100 pl-20">
                                  Error: {errorDetail.error}
                                </td>
                              </tr>
                            )}
                          </React.Fragment>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Final Import Execution Options */}
              <div className="rounded-xl border border-gray-200 bg-gray-50/30 p-5 space-y-4">
                <h4 className="text-sm font-semibold text-gray-900">Final Import Configuration</h4>
                
                <div className="max-w-md">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">
                    Import Safety Mode
                  </label>
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        data-testid="radio-mode-strict"
                        type="radio"
                        name="importMode"
                        value="strict"
                        checked={importMode === 'strict'}
                        onChange={() => setImportMode('strict')}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                      />
                      <div>
                        <span className="text-sm font-semibold text-gray-800">Strict Mode (All-or-Nothing)</span>
                        <span className="block text-xs text-gray-500">Rolls back transaction completely if any row fails. Default.</span>
                      </div>
                    </label>

                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        data-testid="radio-mode-partial"
                        type="radio"
                        name="importMode"
                        value="partial"
                        checked={importMode === 'partial'}
                        onChange={() => setImportMode('partial')}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500"
                      />
                      <div>
                        <span className="text-sm font-semibold text-gray-800">Partial Mode</span>
                        <span className="block text-xs text-gray-500">Creates valid rows, skipping and logging failed rows.</span>
                      </div>
                    </label>
                  </div>
                </div>

                {importMode === 'strict' && dryRunResult.failure_count > 0 && (
                  <div className="rounded-lg bg-red-50 p-3 text-xs text-red-700 flex items-start gap-2">
                    <AlertTriangle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                    <div>
                      <span className="font-semibold block">Strict Mode Blocks Execution</span>
                      Your dry-run has validation errors. In Strict Mode, the import is blocked because the file contains failed rows. Switch to Partial Mode if you want to skip invalid rows and load valid ones, or repair the file and upload again.
                    </div>
                  </div>
                )}
              </div>

              {/* Action buttons */}
              <div className="flex justify-between pt-2">
                <button
                  onClick={() => setStep(2)}
                  className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back to Mapping
                </button>

                <button
                  disabled={loading || (importMode === 'strict' && dryRunResult.failure_count > 0)}
                  onClick={runApplyImport}
                  className="flex items-center gap-2 rounded-lg bg-emerald-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700 disabled:opacity-50 transition shadow-sm"
                >
                  Apply Final Import
                  <CheckCircle2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
