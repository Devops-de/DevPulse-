import React, { useState } from 'react';
import { Send, Terminal, Sparkles, Check } from 'lucide-react';
import { createPulseEvent } from '../services/api';

interface QuickActionsProps {
  onEventCreated: () => void;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ onEventCreated }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('git');
  const [details, setDetails] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [justSubmitted, setJustSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      await createPulseEvent({
        title: title.trim(),
        category,
        status: 'success',
        details: details.trim() || undefined,
      });
      setTitle('');
      setDetails('');
      setJustSubmitted(true);
      setTimeout(() => setJustSubmitted(false), 2000);
      onEventCreated();
    } catch (err) {
      alert('Failed to send pulse event. Ensure FastAPI is running on port 8000.');
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
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Event Title
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Unit tests passed"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition"
            >
              <option value="git">Git / Repository</option>
              <option value="build">Build / Compile</option>
              <option value="test">Testing</option>
              <option value="deploy">Deployment</option>
              <option value="system">System</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Details (Optional)
            </label>
            <input
              type="text"
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              placeholder="e.g. 100% test coverage achieved"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
            />
          </div>

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
