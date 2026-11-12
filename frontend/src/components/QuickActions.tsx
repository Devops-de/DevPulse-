import React, { useEffect, useRef, useState } from 'react';
import { Send, Terminal, Sparkles, Check, AlertCircle } from 'lucide-react';
import { createPulseEvent } from '../services/api';

interface QuickActionsProps {
  onEventCreated: () => void;
}

const EVENT_CATEGORIES = [
  { value: 'git', label: 'Git / Repository' },
  { value: 'build', label: 'Build / Compile' },
  { value: 'test', label: 'Testing' },
  { value: 'deploy', label: 'Deployment' },
  { value: 'system', label: 'System' },
] as const;

export const QuickActions: React.FC<QuickActionsProps> = ({ onEventCreated }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState<string>('git');
  const [details, setDetails] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [justSubmitted, setJustSubmitted] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
      }
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;

    setIsSubmitting(true);
    setErrorMessage(null);
    try {
      await createPulseEvent({
        title: trimmedTitle,
        category,
        status: 'success',
        details: details.trim() || undefined,
      });
      setTitle('');
      setDetails('');
      setJustSubmitted(true);
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
      }
      timerRef.current = window.setTimeout(() => setJustSubmitted(false), 2000);
      onEventCreated();
    } catch (err) {
      const detail = err instanceof Error ? err.message : 'Unable to reach FastAPI backend.';
      setErrorMessage(`Failed to send pulse event (${detail}). Ensure FastAPI is running.`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center space-x-2 mb-2">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <h2 className="text-base font-semibold text-white tracking-tight">Record Pulse Event</h2>
        </div>
        <p className="text-xs text-slate-400 mb-5">
          Trigger a live event to test full-stack communication with FastAPI.
        </p>

        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label htmlFor="pulse-title" className="block text-xs font-medium text-slate-300 mb-1">
              Event Title
            </label>
            <input
              id="pulse-title"
              type="text"
              required
              minLength={2}
              maxLength={100}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Unit tests passed"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div>
            <label htmlFor="pulse-category" className="block text-xs font-medium text-slate-300 mb-1">
              Category
            </label>
            <select
              id="pulse-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition"
            >
              {EVENT_CATEGORIES.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="pulse-details" className="block text-xs font-medium text-slate-300 mb-1">
              Details (Optional)
            </label>
            <input
              id="pulse-details"
              type="text"
              maxLength={500}
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              placeholder="e.g. 100% test coverage achieved"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
            />
          </div>

          {errorMessage && (
            <div
              role="alert"
              className="flex items-start space-x-2 p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs"
            >
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
              <span>{errorMessage}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-2 rounded-lg text-sm transition flex items-center justify-center space-x-2 shadow-md shadow-indigo-600/20"
          >
            {justSubmitted ? (
              <>
                <Check className="w-4 h-4 text-emerald-300" />
                <span>Recorded!</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>{isSubmitting ? 'Posting...' : 'Emit Event'}</span>
              </>
            )}
          </button>
        </form>
      </div>

      <div className="mt-6 pt-4 border-t border-slate-800/80 text-xs text-slate-500 space-y-1">
        <div className="flex items-center space-x-1 text-slate-400 font-medium">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Active Endpoints</span>
        </div>
        <p className="font-mono text-[11px] text-slate-400">GET /api/v1/metrics/pulse</p>
        <p className="font-mono text-[11px] text-slate-400">POST /api/v1/metrics/events</p>
      </div>
    </div>
  );
};
