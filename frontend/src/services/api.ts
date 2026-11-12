import { HealthResponse, MetricSummary, PulseEvent, PulseEventCreate } from '../types/api';

const API_BASE = '/api/v1';

async function requestJson<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    let errorMessage = `${res.status} ${res.statusText}`;
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body?.detail === 'string') {
        errorMessage = body.detail;
      }
    } catch {
      // Response body was not JSON; retain HTTP status text
    }
    throw new Error(`API request failed (${path}): ${errorMessage}`);
  }
  return res.json() as Promise<T>;
}

export function fetchHealth(signal?: AbortSignal): Promise<HealthResponse> {
  return requestJson<HealthResponse>('/health', { signal });
}

export function fetchPulseSummary(signal?: AbortSignal): Promise<MetricSummary> {
  return requestJson<MetricSummary>('/metrics/pulse', { signal });
}

export function fetchEvents(limit: number = 20, signal?: AbortSignal): Promise<PulseEvent[]> {
  return requestJson<PulseEvent[]>(`/metrics/events?limit=${limit}`, { signal });
}

export function createPulseEvent(data: PulseEventCreate): Promise<PulseEvent> {
  return requestJson<PulseEvent>('/metrics/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}
