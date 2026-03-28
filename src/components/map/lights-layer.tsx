"use client";

import { Source, Layer } from "react-map-gl/mapbox";
import { Port } from "@/types";
import { useMemo } from "react";

interface LightsLayerProps {
  ports: Port[];
}

export function LightsLayer({ ports }: LightsLayerProps) {
  const geoJSON = useMemo(() => ({
    type: "FeatureCollection" as const,
    features: ports.map((p) => ({
      type: "Feature" as const,
      properties: { viirs_mean: p.viirs_mean },
      geometry: {
        type: "Point" as const,
        coordinates: [p.lng, p.lat],
      },
    })),
  }), [ports]);

  return (
    <Source id="viirs-overlay" type="geojson" data={geoJSON}>
      <Layer
        id="viirs-circles-overlay"
        type="circle"
        paint={{
          "circle-radius": [
            "interpolate", ["linear"], ["get", "viirs_mean"],
            0, 5, 50, 25,
          ],
          "circle-color": [
            "interpolate", ["linear"], ["get", "viirs_mean"],
            0, "#1a1a2e", 20, "#e2d810", 40, "#ffa500", 60, "#ffffff",
          ],
          "circle-opacity": 0.5,
        }}
      />
    </Source>
  );
}
