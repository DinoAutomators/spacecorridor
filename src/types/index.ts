export interface Port {
  id: string;
  name: string;
  country: string;
  lat: number;
  lng: number;
  harbor_type: string;
  cargo_capability: string[];
  services_score: number;
  strategic_score: number;
  no2_mean: number;
  viirs_mean: number;
}

export interface Corridor {
  id: string;
  name: string;
  from_port_id: string;
  to_port_id: string;
  region: string;
  geometry: GeoJSON.LineString | GeoJSON.MultiLineString;
  description: string;
  from_port?: Port;
  to_port?: Port;
}

export interface CorridorScore {
  id: string;
  corridor_id: string;
  emissions_score: number;
  no2_score: number;
  lights_score: number;
  strategic_score: number;
  feasibility_score: number;
  readiness_score: number;
  bottleneck: string;
  recommendation: string;
  ai_explanation: string;
}

export interface CorridorWithDetails extends Corridor {
  score?: CorridorScore;
  from_port: Port;
  to_port: Port;
}

export interface Filters {
  region: string | null;
  readinessRange: [number, number];
  bottleneck: string | null;
  showNO2Layer: boolean;
  showLightsLayer: boolean;
}

export type BottleneckType =
  | "Port Infrastructure Gap"
  | "Fuel Transition Gap"
  | "Pollution Exposure Hotspot"
  | "Cross-Mode Coordination Gap"
  | "Monitoring/Readiness Gap";
