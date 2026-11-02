import React from 'react';
import { PulseEvent } from '../types/api';
import { CheckCircle2, AlertTriangle, AlertCircle, Info, Clock } from 'lucide-react';

interface PulseActivityProps {
  events: PulseEvent[];
  isLoading: boolean;
}

export const PulseActivity: React.FC<PulseActivityProps> = ({ events, isLoading }) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'success':
        return (
          <span className="flex items-center space-x-1 text-[11px] px-2 py-0.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
            <CheckCircle2 className="w-3 h-3" />
            <span>Success</span>
          </span>
        );
      case 'warning':
        return (
          <span className="flex items-center space-x-1 text-[11px] px-2 py-0.5 rounded-full border border-amber-500/20 bg-amber-500/10 text-amber-400">
            <AlertTriangle className="w-3 h-3" />
            <span>Warning</span>
          </span>
        );
      case 'error':
        return (
          <span className="flex items-center space-x-1 text-[11px] px-2 py-0.5 rounded-full border border-rose-500/20 bg-rose-500/10 text-rose-400">
            <AlertCircle className="w-3 h-3" />
            <span>Error</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center space-x-1 text-[11px] px-2 py-0.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 text-indigo-400">
            <Info className="w-3 h-3" />
            <span>Info</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-base font-semibold text-white tracking-tight">Recent Pulse Stream</h2>
          <p className="text-xs text-slate-400">Live operational events recorded by FastAPI services</p>
        </div>
        <div className="flex items-center space-x-1.5 text-xs text-slate-500">
          <Clock className="w-3.5 h-3.5" />
          <span>Polling 3s</span>
        </div>
      </div>

      {isLoading && events.length === 0 ? (
        <div className="text-sm text-slate-500 text-center py-10">Loading stream...</div>
      ) : events.length === 0 ? (
        <div className="text-sm text-slate-500 text-center py-10">No events captured yet.</div>
      ) : (
        <div className="space-y-3">
          {events.map((ev) => {
            const time = new Date(ev.timestamp).toLocaleTimeString();
            return (
              <div
                key={ev.id}
                className="flex items-start justify-between p-3.5 rounded-lg bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 transition"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    {getStatusBadge(ev.status)}
                    <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">
                      [{ev.category}]
                    </span>
                    <span className="text-sm font-medium text-slate-200">{ev.title}</span>
                  </div>
                  {ev.details && (
                    <p className="text-xs text-slate-400 pl-1">{ev.details}</p>
                  )}
                </div>
                <span className="text-xs font-mono text-slate-500 whitespace-nowrap pl-3">
                  {time}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
