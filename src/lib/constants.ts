export const SCORING_WEIGHTS = {
  emissions: 0.25,
  no2: 0.20,
  lights: 0.20,
  strategic: 0.20,
  feasibility: 0.15,
} as const;

export const BOTTLENECK_CATEGORIES = [
  "Port Infrastructure Gap",
  "Fuel Transition Gap",
  "Pollution Exposure Hotspot",
  "Cross-Mode Coordination Gap",
  "Monitoring/Readiness Gap",
] as const;

export const REGIONS = [
  "Asia-Europe",
  "Trans-Pacific",
  "Regional",
  "Atlantic",
  "Mediterranean",
  "Indian Ocean",
  "Asia-Pacific",
] as const;

export const READINESS_COLORS = {
  high: "#22c55e",    // green-500
  medium: "#f59e0b",  // amber-500
  low: "#ef4444",     // red-500
} as const;

export function getReadinessColor(score: number): string {
  if (score >= 70) return READINESS_COLORS.high;
  if (score >= 40) return READINESS_COLORS.medium;
  return READINESS_COLORS.low;
}

export function getReadinessLabel(score: number): string {
  if (score >= 70) return "High";
  if (score >= 40) return "Medium";
  return "Low";
}

export const SCORE_LABELS: Record<string, string> = {
  emissions_score: "Emissions",
  no2_score: "NO₂ Pollution",
  lights_score: "Night Lights",
  strategic_score: "Strategic Value",
  feasibility_score: "Feasibility",
};

export const BOTTLENECK_ICONS: Record<string, string> = {
  "Port Infrastructure Gap": "building-2",
  "Fuel Transition Gap": "fuel",
  "Pollution Exposure Hotspot": "cloud",
  "Cross-Mode Coordination Gap": "git-branch",
  "Monitoring/Readiness Gap": "activity",
};
