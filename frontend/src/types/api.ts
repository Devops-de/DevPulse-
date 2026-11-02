export interface HealthResponse {
  status: string;
  app_name: string;
  version: string;
  environment: string;
  uptime_seconds: number;
  timestamp: string;
  python_version: string;
}

export interface SystemMetric {
  cpu_percent: number;
  memory_percent: number;
  memory_used_mb: number;
  memory_total_mb: number;
  disk_percent: number;
  platform_name: string;
}

export interface PulseEvent {
  id: string;
  title: string;
  category: string;
  status: 'success' | 'warning' | 'error' | 'info' | string;
  details?: string | null;
  timestamp: string;
}

export interface PulseEventCreate {
  title: string;
  category: string;
  status: 'success' | 'warning' | 'error' | 'info' | string;
  details?: string;
}

export interface ServiceStatus {
  name: string;
  status: 'online' | 'offline' | 'degraded' | string;
  latency_ms: number;
}

export interface MetricSummary {
  system: SystemMetric;
  active_services: ServiceStatus[];
  recent_events: PulseEvent[];
  total_events_recorded: number;
}
