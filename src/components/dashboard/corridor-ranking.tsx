"use client";

import { CorridorWithDetails } from "@/types";
import { CorridorCard } from "./corridor-card";

interface CorridorRankingProps {
  corridors: CorridorWithDetails[];
  selectedCorridorId: string | null;
  onSelectCorridor: (id: string) => void;
}

export function CorridorRanking({
  corridors,
  selectedCorridorId,
  onSelectCorridor,
}: CorridorRankingProps) {
  const sorted = [...corridors].sort(
    (a, b) => (b.score?.readiness_score ?? 0) - (a.score?.readiness_score ?? 0)
  );

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-border/40 px-4 py-3">
        <h2 className="font-semibold text-sm">Corridor Rankings</h2>
        <p className="text-xs text-muted-foreground mt-0.5">
          Sorted by decarbonization readiness
        </p>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {sorted.map((corridor) => (
          <CorridorCard
            key={corridor.id}
            corridor={corridor}
            isSelected={corridor.id === selectedCorridorId}
            onClick={() => onSelectCorridor(corridor.id)}
          />
        ))}
      </div>
    </div>
  );
}
