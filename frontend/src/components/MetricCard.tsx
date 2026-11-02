import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  progress?: number;
  color?: 'indigo' | 'violet' | 'emerald' | 'amber';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  progress,
  color = 'indigo',
}) => {
  const barColors = {
    indigo: 'bg-indigo-500',
    violet: 'bg-violet-500',
    emerald: 'bg-emerald-500',
    amber: 'bg-amber-500',
  }[color];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition shadow-sm">
      <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
        <span>{title}</span>
        <div className="p-1 rounded bg-slate-800/80 text-slate-300">{icon}</div>
      </div>
      <div className="mt-3 flex items-baseline space-x-2">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {subtitle && <span className="text-xs text-slate-400">{subtitle}</span>}
      </div>
      {typeof progress === 'number' && (
        <div className="w-full bg-slate-800 rounded-full h-1.5 mt-3 overflow-hidden">
          <div
            className={`${barColors} h-1.5 rounded-full transition-all duration-500`}
            style={{ width: `${Math.min(Math.max(progress, 0), 100)}%` }}
          />
        </div>
      )}
    </div>
  );
};
