"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb } from "lucide-react";

interface RecommendationCardProps {
  recommendation: string;
}

export function RecommendationCard({ recommendation }: RecommendationCardProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-sm">
          <Lightbulb className="h-4 w-4 text-blue-400" />
          Recommended Intervention
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm leading-relaxed text-muted-foreground">
          {recommendation}
        </p>
      </CardContent>
    </Card>
  );
}
