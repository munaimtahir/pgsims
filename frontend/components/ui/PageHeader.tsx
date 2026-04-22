interface HeaderBadge {
  label: string;
  tone?: 'default' | 'info' | 'success' | 'warning' | 'danger';
}

interface PageHeaderProps {
  title: string;
  description?: string;
  badges?: HeaderBadge[];
  actions?: React.ReactNode;
}

const TONE_CLASSES: Record<NonNullable<HeaderBadge['tone']>, string> = {
  default: 'bg-slate-100 text-slate-700 border-slate-200',
  info: 'bg-indigo-50 text-indigo-700 border-indigo-100',
  success: 'bg-green-50 text-green-700 border-green-100',
  warning: 'bg-orange-50 text-orange-700 border-orange-100',
  danger: 'bg-red-50 text-red-700 border-red-100',
};

export default function PageHeader({ title, description, badges = [], actions }: PageHeaderProps) {
  return (
    <header className="pg-page-header">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <h1 className="pg-page-title">{title}</h1>
          {description ? <p className="pg-page-description">{description}</p> : null}
          {badges.length > 0 ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {badges.map((badge) => {
                const tone = badge.tone ?? 'default';
                return (
                  <span
                    key={`${badge.label}-${tone}`}
                    className={`rounded-full border px-2.5 py-1 text-xs font-medium ${TONE_CLASSES[tone]}`}
                  >
                    {badge.label}
                  </span>
                );
              })}
            </div>
          ) : null}
        </div>
        {actions ? <div className="flex shrink-0 items-center gap-2">{actions}</div> : null}
      </div>
    </header>
  );
}
