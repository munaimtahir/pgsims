'use client';

interface LoadingSkeletonProps {
  lines?: number;
  className?: string;
}

export default function LoadingSkeleton({ lines = 3, className = '' }: LoadingSkeletonProps) {
  return (
    <div className={`animate-pulse ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 rounded mb-2" style={{ width: i === lines - 1 ? '75%' : '100%' }} />
      ))}
    </div>
  );
}

export function TableSkeleton({ rows = 5, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="animate-pulse">
      <div className="space-y-3">
        {/* Header */}
        <div className="flex space-x-4">
          {Array.from({ length: cols }).map((_, i) => (
            <div key={i} className="h-4 bg-gray-300 rounded flex-1" />
          ))}
        </div>
        {/* Rows */}
        {Array.from({ length: rows }).map((_, rowIdx) => (
          <div key={rowIdx} className="flex space-x-4">
            {Array.from({ length: cols }).map((_, colIdx) => (
              <div key={colIdx} className="h-4 bg-gray-200 rounded flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="animate-pulse bg-white rounded-lg shadow p-6">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-4" />
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-2/3" />
    </div>
  );
}
