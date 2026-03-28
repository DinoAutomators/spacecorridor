"use client";

import { Badge } from "@/components/ui/badge";
import { CorridorWithDetails } from "@/types";
import { getReadinessColor, getReadinessLabel } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface CorridorCardProps {
  corridor: CorridorWithDetails;
  isSelected: boolean;
  onClick: () => void;
}

export function CorridorCard({ corridor, isSelected, onClick }: CorridorCardProps) {
  const readiness = corridor.score?.readiness_score ?? 0;
  const color = getReadinessColor(readiness);

  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full text-left rounded-lg border p-3 transition-all hover:bg-accent/50",
        isSelected
          ? "border-blue-500/50 bg-blue-500/5"
          : "border-border/40"
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="font-medium text-sm truncate">{corridor.name}</p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {corridor.from_port?.name} → {corridor.to_port?.name}
          </p>
        </div>
        <Badge variant="outline" className="shrink-0 text-xs">
          {corridor.region}
        </Badge>
      </div>

      <div className="mt-3 space-y-1.5">
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">Readiness</span>
          <span className="font-medium" style={{ color }}>
            {readiness} — {getReadinessLabel(readiness)}
          </span>
        </div>
        <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{
              width: `${readiness}%`,
              backgroundColor: color,
            }}
          />
        </div>
      </div>

      {corridor.score?.bottleneck && (
        <div className="mt-2">
          <Badge
            variant="secondary"
            className="text-[10px] font-normal"
          >
            {corridor.score.bottleneck}
          </Badge>
        </div>
      )}
    </button>
  );
}
