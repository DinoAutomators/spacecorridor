"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { CorridorScore } from "@/types";
import { getReadinessColor } from "@/lib/constants";

interface ScoreBarChartProps {
  score: CorridorScore;
}

export function ScoreBarChart({ score }: ScoreBarChartProps) {
  const data = [
    { name: "Emissions", value: score.emissions_score },
    { name: "NO₂", value: score.no2_score },
    { name: "Lights", value: score.lights_score },
    { name: "Strategic", value: score.strategic_score },
    { name: "Feasibility", value: score.feasibility_score },
  ];

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} layout="vertical" margin={{ left: 70, right: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
        <XAxis
          type="number"
          domain={[0, 100]}
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
        />
        <YAxis
          dataKey="name"
          type="category"
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
          width={65}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
          {data.map((entry) => (
            <Cell key={entry.name} fill={getReadinessColor(entry.value)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
