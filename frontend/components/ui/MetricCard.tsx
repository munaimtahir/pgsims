interface MetricCardProps {
  label: string;
  value: string | number;
  hint?: string;
  tone?: 'default' | 'info' | 'success' | 'warning' | 'danger';
}

const BORDER_TONES: Record<NonNullable<MetricCardProps['tone']>, string> = {
  default: 'border-slate-200',
  info: 'border-indigo-200',
  success: 'border-green-200',
  warning: 'border-orange-200',
  danger: 'border-red-200',
};

export default function MetricCard({ label, value, hint, tone = 'default' }: MetricCardProps) {
  return (
    <div className={`pg-kpi-card ${BORDER_TONES[tone]}`}>
      <p className="pg-kpi-value">{value}</p>
      <p className="pg-kpi-label">{label}</p>
      {hint ? <p className="mt-1 text-xs text-slate-500">{hint}</p> : null}
    </div>
  );
}
