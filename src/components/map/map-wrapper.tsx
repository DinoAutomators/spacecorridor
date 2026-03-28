"use client";

import dynamic from "next/dynamic";
import { CorridorWithDetails, Port } from "@/types";

const CorridorMap = dynamic(
  () => import("./corridor-map").then((mod) => mod.CorridorMap),
  { ssr: false, loading: () => <MapSkeleton /> }
);

function MapSkeleton() {
  return (
    <div className="flex h-full w-full items-center justify-center bg-card animate-pulse rounded-lg">
      <p className="text-muted-foreground text-sm">Loading map...</p>
    </div>
  );
}

interface MapWrapperProps {
  corridors: CorridorWithDetails[];
  ports: Port[];
  selectedCorridorId: string | null;
  onSelectCorridor: (id: string) => void;
  showNO2Layer: boolean;
  showLightsLayer: boolean;
}

export function MapWrapper(props: MapWrapperProps) {
  return (
    <div className="h-full w-full rounded-lg overflow-hidden border border-border/40">
      <CorridorMap {...props} />
    </div>
  );
}
