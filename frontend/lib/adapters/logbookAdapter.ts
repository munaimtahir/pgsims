import type { LogbookEntry, PendingLogbookEntry } from '@/lib/api/logbook';

export interface UILogbookEntry extends LogbookEntry {
  feedback_text: string | null;
  submitted_display_at: string | null;
}

export interface UIPendingLogbookEntry extends PendingLogbookEntry {
  feedback_text: string | null;
}

export function adaptLogbookEntry(input: Partial<LogbookEntry>): UILogbookEntry {
  const feedback =
    input.feedback ??
    input.supervisor_feedback ??
    input.supervisor_comments ??
    null;

  return {
    id: Number(input.id ?? 0),
    case_title: input.case_title ?? '',
    date: input.date ?? '',
    location_of_activity: input.location_of_activity ?? '',
    patient_history_summary: input.patient_history_summary ?? '',
    management_action: input.management_action ?? '',
    topic_subtopic: input.topic_subtopic ?? '',
    user: input.user,
    rotation: input.rotation,
    submitted_at: input.submitted_at,
    status: (input.status as UILogbookEntry['status']) ?? 'draft',
    verified_by: input.verified_by,
    verified_at: input.verified_at,
    feedback: input.feedback,
    supervisor_feedback: input.supervisor_feedback,
    supervisor_comments: input.supervisor_comments,
    updated_at: input.updated_at,
    created_at: input.created_at,
    submitted_to_supervisor_at: input.submitted_to_supervisor_at,
    feedback_text: feedback,
    submitted_display_at: input.submitted_at ?? input.submitted_to_supervisor_at ?? null,
  };
}

export function adaptLogbookEntryList(
  data: { results?: LogbookEntry[] } | LogbookEntry[]
): UILogbookEntry[] {
  const rows = Array.isArray(data) ? data : data.results ?? [];
  return rows.map(adaptLogbookEntry);
}

export function adaptPendingLogbookEntry(
  input: PendingLogbookEntry & {
    feedback?: string | null;
    supervisor_feedback?: string | null;
  }
): UIPendingLogbookEntry {
  return {
    ...input,
    feedback_text: input.feedback ?? input.supervisor_feedback ?? null,
  };
}

export function adaptPendingLogbookList(data: {
  count: number;
  results: (PendingLogbookEntry & { feedback?: string | null; supervisor_feedback?: string | null })[];
}) {
  return {
    ...data,
    results: data.results.map(adaptPendingLogbookEntry),
  };
}

