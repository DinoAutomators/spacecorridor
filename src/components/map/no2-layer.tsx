"use client";

import { Source, Layer } from "react-map-gl/mapbox";
import { Port } from "@/types";
import { useMemo } from "react";

interface NO2LayerProps {
  ports: Port[];
}

export function NO2Layer({ ports }: NO2LayerProps) {
  const geoJSON = useMemo(() => ({
    type: "FeatureCollection" as const,
    features: ports.map((p) => ({
      type: "Feature" as const,
      properties: { no2_mean: p.no2_mean },
      geometry: {
        type: "Point" as const,
        coordinates: [p.lng, p.lat],
      },
    })),
  }), [ports]);

  return (
    <Source id="no2-overlay" type="geojson" data={geoJSON}>
      <Layer
        id="no2-heatmap-overlay"
        type="heatmap"
        paint={{
          "heatmap-weight": [
            "interpolate", ["linear"], ["get", "no2_mean"],
            0, 0, 100, 1,
          ],
          "heatmap-intensity": 1,
          "heatmap-radius": 40,
          "heatmap-opacity": 0.6,
        }}
      />
    </Source>
  );
}
