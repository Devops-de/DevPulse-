import React from 'react';
import { X, Info, ShieldCheck, Cpu, Code2, Server, HeartHandshake } from 'lucide-react';

interface AboutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div 
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Info className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-white tracking-tight">About DevPulse</h3>
              <p className="text-xs text-slate-400">Decoupled Developer Telemetry &amp; System Observability</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="px-6 py-5 overflow-y-auto space-y-5 text-sm text-slate-300">
          
          {/* Mission */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-2">Project Vision</h4>
            <p className="text-slate-300 leading-relaxed text-xs sm:text-sm">
              <strong>DevPulse</strong> is an open-source, high-performance developer observability and system telemetry platform. It bridges the gap between local development and cloud-native monitoring by providing real-time hardware telemetry and event instrumentation without requiring complex enterprise SaaS monitoring agents.
            </p>
          </div>

          {/* Key Pillars */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
              <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs">
                <Cpu className="w-4 h-4" />
                <span>Zero-Overhead Metrics</span>
              </div>
              <p className="text-xs text-slate-400">
                Samples system telemetry (CPU, RAM, disk, uptime) with lightweight OS counters and exports via Prometheus RFC 0.0.4 format.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
              <div className="flex items-center space-x-2 text-emerald-400 font-semibold text-xs">
                <ShieldCheck className="w-4 h-4" />
                <span>Zero Personal Data</span>
              </div>
              <p className="text-xs text-slate-400">
                Operates strictly with anonymous machine counters. No personal data, tracking cookies, or external telemetry exfiltration.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
              <div className="flex items-center space-x-2 text-violet-400 font-semibold text-xs">
                <Code2 className="w-4 h-4" />
                <span>Decoupled Architecture</span>
              </div>
              <p className="text-xs text-slate-400">
                Modular Python FastAPI backend enforcing strict Pydantic v2 schemas paired with a typed React 18 TypeScript SPA.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
              <div className="flex items-center space-x-2 text-amber-400 font-semibold text-xs">
                <Server className="w-4 h-4" />
                <span>Cloud-Ready DevOps</span>
              </div>
              <p className="text-xs text-slate-400">
                Equipped with Docker Compose, Kubernetes manifests with health probes, and Terraform AWS ECS/CloudWatch configurations.
              </p>
            </div>
          </div>

          {/* Tech Stack Pills */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Core Technologies</h4>
            <div className="flex flex-wrap gap-1.5 text-xs font-mono">
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Python 3.12</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">FastAPI</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Pydantic v2</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">React 18</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">TypeScript 5</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Tailwind CSS</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Vite</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Docker</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Kubernetes</span>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 border border-slate-700">Terraform</span>
            </div>
          </div>

          {/* Licensing & Open Source */}
          <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center space-x-1.5">
              <HeartHandshake className="w-4 h-4 text-rose-400" />
              <span>Dual Licensed: <strong>MIT</strong> &amp; <strong>Apache 2.0</strong></span>
            </span>
            <span className="font-mono text-[11px] text-slate-400">Version 0.1.0</span>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 border-t border-slate-800 bg-slate-900/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
