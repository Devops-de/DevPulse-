import React from 'react';
import { Activity, ExternalLink, Info } from 'lucide-react';
import { HealthResponse } from '../types/api';

interface HeaderProps {
  health: HealthResponse | null;
  isLoading: boolean;
  onOpenAbout?: () => void;
}

const API_ORIGIN = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const Header: React.FC<HeaderProps> = ({ health, isLoading, onOpenAbout }) => {
  const isOnline = Boolean(health);
  const badgeStyle = isLoading
    ? 'border-amber-500/20 bg-amber-500/10 text-amber-400'
    : isOnline
      ? 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400'
      : 'border-rose-500/20 bg-rose-500/10 text-rose-400';
  const dotStyle = isLoading ? 'bg-amber-400' : isOnline ? 'bg-emerald-400' : 'bg-rose-400';

  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Activity className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                DevPulse
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
                {health?.version || 'v0.1.0'}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              FastAPI + React Telemetry Starter
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div
            className={`flex items-center space-x-2 text-xs px-3 py-1.5 rounded-full border ${badgeStyle}`}
          >
            <span className={`w-2 h-2 rounded-full pulse-indicator ${dotStyle}`} />
            <span className="font-medium">
              {isLoading ? 'Connecting...' : isOnline ? 'FastAPI Online' : 'Backend Disconnected'}
            </span>
          </div>

          <button
            type="button"
            onClick={onOpenAbout}
            className="inline-flex items-center space-x-1.5 text-xs font-medium px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition"
            aria-label="About DevPulse"
          >
            <Info className="w-3.5 h-3.5 text-indigo-400" />
            <span>About</span>
          </button>

          <a
            href={`${API_ORIGIN}/docs`}
            target="_blank"
            rel="noreferrer"
            className="hidden sm:inline-flex items-center space-x-1.5 text-xs font-medium px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm shadow-indigo-600/30"
          >
            <span>Swagger Docs</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </header>
  );
};
