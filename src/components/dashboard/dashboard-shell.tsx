"use client";

import { useState, useMemo } from "react";
import { CorridorWithDetails, Port, Filters } from "@/types";
import { MapWrapper } from "@/components/map/map-wrapper";
import { SummaryCards } from "./summary-cards";
import { CorridorRanking } from "./corridor-ranking";
import { FiltersBar } from "./filters-bar";
import { CorridorDetail } from "@/components/corridor/corridor-detail";

interface DashboardShellProps {
  corridors: CorridorWithDetails[];
  ports: Port[];
}

export function DashboardShell({ corridors, ports }: DashboardShellProps) {
  const [selectedCorridorId, setSelectedCorridorId] = useState<string | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [filters, setFilters] = useState<Filters>({
    region: null,
    readinessRange: [0, 100],
    bottleneck: null,
    showNO2Layer: false,
    showLightsLayer: false,
  });

  const filteredCorridors = useMemo(() => {
    return corridors.filter((c) => {
      if (filters.region && c.region !== filters.region) return false;
      if (filters.bottleneck && c.score?.bottleneck !== filters.bottleneck) return false;
      const readiness = c.score?.readiness_score ?? 0;
      if (readiness < filters.readinessRange[0] || readiness > filters.readinessRange[1])
        return false;
      return true;
    });
  }, [corridors, filters]);

  const selectedCorridor = corridors.find((c) => c.id === selectedCorridorId) ?? null;

  const handleSelectCorridor = (id: string) => {
    setSelectedCorridorId(id);
    setDetailOpen(true);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col">
      <div className="border-b border-border/40 px-4 py-3">
        <FiltersBar filters={filters} onFiltersChange={setFilters} />
      </div>

      <div className="px-4 py-3">
        <SummaryCards corridors={filteredCorridors} />
      </div>

      <div className="flex flex-1 min-h-0 gap-0">
        <div className="flex-1 p-4 pt-0">
          <MapWrapper
            corridors={filteredCorridors}
            ports={ports}
            selectedCorridorId={selectedCorridorId}
            onSelectCorridor={handleSelectCorridor}
            showNO2Layer={filters.showNO2Layer}
            showLightsLayer={filters.showLightsLayer}
          />
        </div>

        <div className="w-80 border-l border-border/40 hidden lg:block">
          <CorridorRanking
            corridors={filteredCorridors}
            selectedCorridorId={selectedCorridorId}
            onSelectCorridor={handleSelectCorridor}
          />
        </div>
      </div>

      <CorridorDetail
        corridor={selectedCorridor}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
      />
    </div>
  );
}
