import { BottleneckType } from "@/types";
import { SCORING_WEIGHTS } from "./constants";

export function computeReadinessScore(scores: {
  emissions_score: number;
  no2_score: number;
  lights_score: number;
  strategic_score: number;
  feasibility_score: number;
}): number {
  return Math.round(
    scores.emissions_score * SCORING_WEIGHTS.emissions +
    scores.no2_score * SCORING_WEIGHTS.no2 +
    scores.lights_score * SCORING_WEIGHTS.lights +
    scores.strategic_score * SCORING_WEIGHTS.strategic +
    scores.feasibility_score * SCORING_WEIGHTS.feasibility
  );
}

export function classifyBottleneck(scores: {
  emissions_score: number;
  no2_score: number;
  lights_score: number;
  strategic_score: number;
  feasibility_score: number;
}): BottleneckType {
  const entries: [string, number][] = [
    ["emissions_score", scores.emissions_score],
    ["no2_score", scores.no2_score],
    ["lights_score", scores.lights_score],
    ["strategic_score", scores.strategic_score],
    ["feasibility_score", scores.feasibility_score],
  ];

  const lowest = entries.reduce((min, e) => (e[1] < min[1] ? e : min));

  const mapping: Record<string, BottleneckType> = {
    emissions_score: "Fuel Transition Gap",
    no2_score: "Pollution Exposure Hotspot",
    lights_score: "Monitoring/Readiness Gap",
    strategic_score: "Cross-Mode Coordination Gap",
    feasibility_score: "Port Infrastructure Gap",
  };

  return mapping[lowest[0]];
}

const RECOMMENDATION_MAP: Record<BottleneckType, string> = {
  "Port Infrastructure Gap":
    "Prioritize shore power installations and LNG bunkering infrastructure at endpoint ports. Consider public-private partnerships for green port upgrades.",
  "Fuel Transition Gap":
    "Accelerate alternative fuel adoption through methanol/ammonia bunkering pilots. Establish green fuel corridors with bilateral agreements between port states.",
  "Pollution Exposure Hotspot":
    "Implement Emission Control Area (ECA) designation along corridor. Deploy real-time emissions monitoring and enforce slow steaming zones near ports.",
  "Cross-Mode Coordination Gap":
    "Develop intermodal digital freight platforms connecting maritime, rail, and road. Align customs procedures for seamless green corridor certification.",
  "Monitoring/Readiness Gap":
    "Deploy satellite-based MRV (Monitoring, Reporting, Verification) systems. Establish corridor-level emissions baselines using Sentinel-5P and AIS data fusion.",
};

export function getRecommendation(bottleneck: BottleneckType): string {
  return RECOMMENDATION_MAP[bottleneck];
}

export function getScoreColor(score: number): string {
  if (score >= 70) return "text-green-400";
  if (score >= 40) return "text-amber-400";
  return "text-red-400";
}

export function getScoreBgColor(score: number): string {
  if (score >= 70) return "bg-green-500";
  if (score >= 40) return "bg-amber-500";
  return "bg-red-500";
}
