'use client';

interface SectionCardProps {
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
}

export default function SectionCard({ title, children, actions, className = '' }: SectionCardProps) {
  return (
    <div className={`bg-white shadow rounded-lg ${className}`}>
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
        <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
        {actions && <div>{actions}</div>}
      </div>
      <div className="px-4 py-5 sm:p-6">{children}</div>
    </div>
  );
}
