import { HealthResponse, MetricSummary, PulseEvent, PulseEventCreate } from '../types/api';

const API_BASE = '/api/v1';

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchPulseSummary(): Promise<MetricSummary> {
  const res = await fetch(`${API_BASE}/metrics/pulse`);
  if (!res.ok) throw new Error(`Pulse query failed: ${res.statusText}`);
  return res.json();
}

export async function fetchEvents(limit: number = 20): Promise<PulseEvent[]> {
  const res = await fetch(`${API_BASE}/metrics/events?limit=${limit}`);
  if (!res.ok) throw new Error(`Events query failed: ${res.statusText}`);
  return res.json();
}

export async function createPulseEvent(data: PulseEventCreate): Promise<PulseEvent> {
  const res = await fetch(`${API_BASE}/metrics/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`Event creation failed: ${res.statusText}`);
  return res.json();
}
