'use client';

export default function ReadonlyNotice({
  children,
}: {
  children?: React.ReactNode;
}) {
  return (
    <div
      data-testid="readonly-notice"
      className="mb-4 rounded-lg border border-blue-200 bg-blue-50 p-3 text-sm text-blue-800"
    >
      {children ?? 'Read-only oversight: mutation actions are hidden for UTRMC users.'}
    </div>
  );
}
