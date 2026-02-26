import type { RotationSummary } from '@/lib/api/rotations';

type NestedRef = { id: number; name: string; code?: string | null };

export interface UIRotationSummary extends RotationSummary {
  department: NestedRef;
  hospital: NestedRef;
}

function normalizeRef(value: unknown, fallbackName: string): NestedRef {
  if (value && typeof value === 'object') {
    const obj = value as Record<string, unknown>;
    return {
      id: typeof obj.id === 'number' ? obj.id : 0,
      name: typeof obj.name === 'string' && obj.name ? obj.name : fallbackName,
      code: typeof obj.code === 'string' ? obj.code : null,
    };
  }

  if (typeof value === 'string' && value.trim()) {
    return { id: 0, name: value.trim(), code: null };
  }

  return { id: 0, name: fallbackName, code: null };
}

export function adaptRotationSummary(input: Partial<RotationSummary>): UIRotationSummary {
  return {
    id: Number(input.id ?? 0),
    name: input.name ?? '',
    department: normalizeRef(input.department, 'Unknown Department'),
    hospital: normalizeRef(input.hospital, 'Unknown Hospital'),
    start_date: input.start_date ?? '',
    end_date: input.end_date ?? '',
    status: input.status ?? 'planned',
    supervisor_name: input.supervisor_name ?? null,
    requires_utrmc_approval: Boolean(input.requires_utrmc_approval),
    override_reason: input.override_reason ?? null,
  };
}

export function adaptRotationList(data: { results?: RotationSummary[] }) {
  return (data.results ?? []).map(adaptRotationSummary);
}

