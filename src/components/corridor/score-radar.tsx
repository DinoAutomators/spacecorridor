"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";
import { CorridorScore } from "@/types";

interface ScoreRadarProps {
  score: CorridorScore;
}

export function ScoreRadar({ score }: ScoreRadarProps) {
  const data = [
    { subject: "Emissions", value: score.emissions_score },
    { subject: "NO2", value: score.no2_score },
    { subject: "Lights", value: score.lights_score },
    { subject: "Strategic", value: score.strategic_score },
    { subject: "Feasibility", value: score.feasibility_score },
  ];

  return (
    <ResponsiveContainer width="100%" height={250}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
        <PolarGrid stroke="hsl(var(--border))" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }}
        />
        <Radar
          name="Score"
          dataKey="value"
          stroke="#3b82f6"
          fill="#3b82f6"
          fillOpacity={0.3}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
