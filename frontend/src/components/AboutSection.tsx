import React from 'react';
import { Info, BookOpen, Sparkles, ShieldCheck, Server } from 'lucide-react';

interface AboutSectionProps {
  onOpenModal: () => void;
}

export const AboutSection: React.FC<AboutSectionProps> = ({ onOpenModal }) => {
  return (
    <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Info className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">About DevPulse</h2>
            <p className="text-xs text-slate-400">
              Decoupled developer telemetry &amp; cloud observability starter
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onOpenModal}
          className="inline-flex items-center self-start sm:self-auto space-x-2 text-xs font-medium px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm"
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>Full Specifications &amp; Overview</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-200 uppercase tracking-wider">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>The Vision</span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            DevPulse offers an ultra-lightweight, self-hosted alternative to heavy enterprise APM
            suites. It delivers immediate local observability for backend services, containers, and
            development environments with zero cloud vendor lock-in.
          </p>
        </div>

        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-200 uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Privacy &amp; Compliance</span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Strictly anonymous, local-only machine counters. Absolutely zero Personally Identifiable
            Information (PII) collection, zero external tracking pixels, and zero AI/ML training
            infrastructure.
          </p>
        </div>

        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-200 uppercase tracking-wider">
            <Server className="w-4 h-4 text-violet-400" />
            <span>Production Architecture</span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Asynchronous FastAPI ASGI runtime exposing standard Prometheus exposition metrics (
            <code className="text-slate-300">/metrics</code>), paired with a reactive React 18
            TypeScript SPA and automated GitHub Actions CI/CD.
          </p>
        </div>
      </div>
    </section>
  );
};
