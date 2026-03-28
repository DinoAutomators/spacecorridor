"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle } from "lucide-react";

interface BottleneckCardProps {
  bottleneck: string;
  scores: {
    emissions_score: number;
    no2_score: number;
    lights_score: number;
    strategic_score: number;
    feasibility_score: number;
  };
}

export function BottleneckCard({ bottleneck, scores }: BottleneckCardProps) {
  const allScores = [
    scores.emissions_score,
    scores.no2_score,
    scores.lights_score,
    scores.strategic_score,
    scores.feasibility_score,
  ];
  const minScore = Math.min(...allScores);
  const severity = minScore < 30 ? "Critical" : minScore < 50 ? "Moderate" : "Low";
  const severityColor =
    severity === "Critical"
      ? "text-red-400 border-red-400/30"
      : severity === "Moderate"
        ? "text-amber-400 border-amber-400/30"
        : "text-green-400 border-green-400/30";

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-sm">
          <AlertTriangle className="h-4 w-4 text-amber-400" />
          Bottleneck Diagnosis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex items-center gap-2">
          <Badge variant="outline">{bottleneck}</Badge>
          <Badge variant="outline" className={severityColor}>
            {severity}
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground">
          The lowest-scoring dimension ({minScore}/100) identifies this
          corridor&apos;s primary barrier to decarbonization readiness.
        </p>
      </CardContent>
    </Card>
  );
}
