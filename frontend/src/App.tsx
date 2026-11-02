import { useEffect, useState, useCallback } from 'react';
import { Header } from './components/Header';
import { MetricCard } from './components/MetricCard';
import { PulseActivity } from './components/PulseActivity';
import { QuickActions } from './components/QuickActions';
import { fetchHealth, fetchPulseSummary } from './services/api';
import { HealthResponse, MetricSummary } from './types/api';
import { Cpu, HardDrive, Server, Layers, ShieldCheck } from 'lucide-react';

export function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [pulse, setPulse] = useState<MetricSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const [healthData, pulseData] = await Promise.all([
        fetchHealth().catch(() => null),
        fetchPulseSummary().catch(() => null),
      ]);
      if (healthData) setHealth(healthData);
      if (pulseData) setPulse(pulseData);
    } catch (err) {
      console.error('Error fetching dashboard telemetry:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    const timer = setInterval(loadData, 3000);
    return () => clearInterval(timer);
  }, [loadData]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header health={health} isLoading={isLoading} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Banner */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 p-6 sm:p-8">
          <div className="max-w-2xl">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              DevPulse <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">Full-Stack Starter</span>
            </h1>
            <p className="mt-2 text-slate-400 text-sm sm:text-base leading-relaxed">
              Modular Python FastAPI backend paired with a Vite + React TypeScript dashboard.
              Ready for immediate extension with clean architecture, typed schemas, and real-time pulse monitoring.
            </p>
            <div className="mt-4 flex flex-wrap gap-2 text-xs font-mono text-slate-300">
              <span className="px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/60">FastAPI</span>
              <span className="px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/60">React 18</span>
              <span className="px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/60">TypeScript</span>
              <span className="px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700/60">Tailwind CSS</span>
            </div>
          </div>
        </div>

        {/* Top Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="API Uptime"
            value={health ? `${Math.floor(health.uptime_seconds)}s` : '0s'}
            subtitle={health?.environment ? `Env: ${health.environment}` : 'Connecting...'}
            icon={<Server className="w-4 h-4 text-emerald-400" />}
            color="emerald"
          />
          <MetricCard
            title="CPU Utilization"
            value={pulse ? `${pulse.system.cpu_percent}%` : '0%'}
            progress={pulse?.system.cpu_percent || 0}
            icon={<Cpu className="w-4 h-4 text-indigo-400" />}
            color="indigo"
          />
          <MetricCard
            title="Memory Usage"
            value={pulse ? `${pulse.system.memory_percent}%` : '0%'}
            subtitle={pulse ? `${pulse.system.memory_used_mb} MB used` : ''}
            progress={pulse?.system.memory_percent || 0}
            icon={<HardDrive className="w-4 h-4 text-violet-400" />}
            color="violet"
          />
          <MetricCard
            title="Recorded Events"
            value={pulse ? pulse.total_events_recorded : 0}
            subtitle={pulse ? `OS: ${pulse.system.platform_name.split(' ')[0]}` : ''}
            icon={<Layers className="w-4 h-4 text-amber-400" />}
            color="amber"
          />
        </div>

        {/* Services Status Pills */}
        {pulse?.active_services && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center gap-4">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center space-x-1.5">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              <span>Core Services:</span>
            </span>
            {pulse.active_services.map((svc) => (
              <div
                key={svc.name}
                className="flex items-center space-x-2 text-xs bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800"
              >
                <span className="w-2 h-2 rounded-full bg-emerald-400 pulse-indicator" />
                <span className="text-slate-200 font-medium">{svc.name}</span>
                <span className="text-slate-500 font-mono text-[11px]">{svc.latency_ms}ms</span>
              </div>
            ))}
          </div>
        )}

        {/* Main Grid: Stream & Action */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <PulseActivity
              events={pulse?.recent_events || []}
              isLoading={isLoading}
            />
          </div>
          <div>
            <QuickActions onEventCreated={loadData} />
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        DevPulse Boilerplate — Built with FastAPI &amp; React
      </footer>
    </div>
  );
}

export default App;
