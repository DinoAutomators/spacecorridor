"use client";

import { Card, CardContent } from "@/components/ui/card";
import { CorridorWithDetails } from "@/types";
import { Ship, TrendingUp, AlertTriangle, Trophy } from "lucide-react";
import { useEffect, useState } from "react";
import { getReadinessColor } from "@/lib/constants";

interface SummaryCardsProps {
  corridors: CorridorWithDetails[];
}

function AnimatedNumber({ value, suffix = "" }: { value: number; suffix?: string }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const duration = 1000;
    const steps = 30;
    const increment = value / steps;
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setDisplay(value);
        clearInterval(timer);
      } else {
        setDisplay(Math.round(current * 10) / 10);
      }
    }, duration / steps);
    return () => clearInterval(timer);
  }, [value]);

  return <span>{display % 1 === 0 ? display : display.toFixed(1)}{suffix}</span>;
}

export function SummaryCards({ corridors }: SummaryCardsProps) {
  const avgReadiness =
    corridors.reduce((sum, c) => sum + (c.score?.readiness_score ?? 0), 0) /
    (corridors.length || 1);

  const bottleneckCounts: Record<string, number> = {};
  corridors.forEach((c) => {
    if (c.score?.bottleneck) {
      bottleneckCounts[c.score.bottleneck] = (bottleneckCounts[c.score.bottleneck] || 0) + 1;
    }
  });
  const topBottleneck = Object.entries(bottleneckCounts).sort(
    (a, b) => b[1] - a[1]
  )[0]?.[0] ?? "N/A";

  const bestCorridor = corridors.reduce(
    (best, c) =>
      (c.score?.readiness_score ?? 0) > (best.score?.readiness_score ?? 0) ? c : best,
    corridors[0]
  );

  const cards = [
    {
      label: "Corridors Analyzed",
      value: corridors.length,
      icon: Ship,
      color: "text-blue-400",
    },
    {
      label: "Avg Readiness",
      value: Math.round(avgReadiness * 10) / 10,
      icon: TrendingUp,
      color: "text-emerald-400",
    },
    {
      label: "Top Bottleneck",
      value: topBottleneck,
      icon: AlertTriangle,
      color: "text-amber-400",
      isText: true,
    },
    {
      label: "Highest Readiness",
      value: bestCorridor?.name ?? "N/A",
      icon: Trophy,
      color: "text-green-400",
      isText: true,
      subValue: bestCorridor?.score?.readiness_score,
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {cards.map((card) => (
        <Card
          key={card.label}
          className="group hover:border-border/80 transition-all hover:shadow-md hover:shadow-blue-500/5"
        >
          <CardContent className="flex items-start gap-3 p-4">
            <card.icon className={`h-5 w-5 mt-0.5 ${card.color}`} />
            <div className="min-w-0">
              <p className="text-xs text-muted-foreground">{card.label}</p>
              {card.isText ? (
                <p className="text-sm font-medium truncate mt-0.5">
                  {card.value}
                  {card.subValue !== undefined && (
                    <span
                      className="ml-1 text-xs"
                      style={{ color: getReadinessColor(card.subValue) }}
                    >
                      ({card.subValue})
                    </span>
                  )}
                </p>
              ) : (
                <p className="text-2xl font-bold mt-0.5">
                  <AnimatedNumber value={card.value as number} />
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
