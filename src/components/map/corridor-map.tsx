"use client";

import { useCallback, useMemo, useRef } from "react";
import Map, {
  Source,
  Layer,
  MapRef,
  MapMouseEvent,
  Popup,
} from "react-map-gl/mapbox";
import "mapbox-gl/dist/mapbox-gl.css";
import { CorridorWithDetails, Port } from "@/types";
import {
  MAPBOX_STYLE,
  INITIAL_VIEW_STATE,
  CORRIDOR_LINE_PAINT,
  PORT_CIRCLE_PAINT,
} from "@/lib/mapbox-config";
import { getReadinessColor } from "@/lib/constants";
import { useState } from "react";

interface CorridorMapProps {
  corridors: CorridorWithDetails[];
  ports: Port[];
  selectedCorridorId: string | null;
  onSelectCorridor: (id: string) => void;
  showNO2Layer: boolean;
  showLightsLayer: boolean;
}

export function CorridorMap({
  corridors,
  ports,
  selectedCorridorId,
  onSelectCorridor,
  showNO2Layer,
  showLightsLayer,
}: CorridorMapProps) {
  const mapRef = useRef<MapRef>(null);
  const [hoveredPort, setHoveredPort] = useState<Port | null>(null);
  const [popupCoords, setPopupCoords] = useState<{ lng: number; lat: number } | null>(null);

  const corridorGeoJSON = useMemo(() => ({
    type: "FeatureCollection" as const,
    features: corridors.map((c) => ({
      type: "Feature" as const,
      id: c.id,
      properties: {
        id: c.id,
        name: c.name,
        readiness: c.score?.readiness_score ?? 0,
        color: getReadinessColor(c.score?.readiness_score ?? 0),
        selected: c.id === selectedCorridorId ? 1 : 0,
      },
      geometry: c.geometry,
    })),
  }), [corridors, selectedCorridorId]);

  const portGeoJSON = useMemo(() => ({
    type: "FeatureCollection" as const,
    features: ports.map((p) => ({
      type: "Feature" as const,
      properties: {
        id: p.id,
        name: p.name,
        country: p.country,
        no2_mean: p.no2_mean,
        viirs_mean: p.viirs_mean,
      },
      geometry: {
        type: "Point" as const,
        coordinates: [p.lng, p.lat],
      },
    })),
  }), [ports]);

  const handleCorridorClick = useCallback(
    (e: MapMouseEvent) => {
      const feature = e.features?.[0];
      if (feature?.properties?.id) {
        const id = feature.properties.id;
        onSelectCorridor(id);
        const corridor = corridors.find((c) => c.id === id);
        if (corridor && mapRef.current) {
          const coords = corridor.geometry.coordinates;
          const midIdx = Math.floor(coords.length / 2);
          mapRef.current.flyTo({
            center: [coords[midIdx][0], coords[midIdx][1]],
            zoom: 4,
            duration: 1500,
          });
        }
      }
    },
    [corridors, onSelectCorridor]
  );

  const handlePortHover = useCallback(
    (e: MapMouseEvent) => {
      const feature = e.features?.[0];
      if (feature?.properties) {
        const port = ports.find((p) => p.id === feature.properties!.id);
        if (port) {
          setHoveredPort(port);
          setPopupCoords({ lng: port.lng, lat: port.lat });
        }
      }
    },
    [ports]
  );

  const handlePortLeave = useCallback(() => {
    setHoveredPort(null);
    setPopupCoords(null);
  }, []);

  return (
    <Map
      ref={mapRef}
      initialViewState={INITIAL_VIEW_STATE}
      style={{ width: "100%", height: "100%" }}
      mapStyle={MAPBOX_STYLE}
      mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_TOKEN}
      interactiveLayerIds={["corridor-lines", "port-circles"]}
      onClick={handleCorridorClick}
      onMouseMove={handlePortHover}
      onMouseLeave={handlePortLeave}
      cursor="pointer"
    >
      <Source id="corridors" type="geojson" data={corridorGeoJSON}>
        <Layer
          id="corridor-lines"
          type="line"
          paint={{
            ...CORRIDOR_LINE_PAINT,
            "line-color": ["get", "color"],
            "line-width": [
              "case",
              ["==", ["get", "selected"], 1],
              5,
              3,
            ],
          }}
        />
      </Source>

      <Source id="ports" type="geojson" data={portGeoJSON}>
        <Layer id="port-circles" type="circle" paint={PORT_CIRCLE_PAINT} />
      </Source>

      {showNO2Layer && (
        <Source id="no2-data" type="geojson" data={portGeoJSON}>
          <Layer
            id="no2-heatmap"
            type="heatmap"
            paint={{
              "heatmap-weight": [
                "interpolate",
                ["linear"],
                ["get", "no2_mean"],
                0, 0,
                100, 1,
              ],
              "heatmap-intensity": 1,
              "heatmap-radius": 40,
              "heatmap-opacity": 0.6,
              "heatmap-color": [
                "interpolate",
                ["linear"],
                ["heatmap-density"],
                0, "rgba(0,0,0,0)",
                0.2, "rgba(103,169,207,0.4)",
                0.4, "rgba(209,229,143,0.6)",
                0.6, "rgba(254,224,76,0.7)",
                0.8, "rgba(253,141,60,0.8)",
                1, "rgba(227,26,28,0.9)",
              ],
            }}
          />
        </Source>
      )}

      {showLightsLayer && (
        <Source id="viirs-data" type="geojson" data={portGeoJSON}>
          <Layer
            id="viirs-circles"
            type="circle"
            paint={{
              "circle-radius": [
                "interpolate",
                ["linear"],
                ["get", "viirs_mean"],
                0, 5,
                50, 25,
              ],
              "circle-color": [
                "interpolate",
                ["linear"],
                ["get", "viirs_mean"],
                0, "#1a1a2e",
                10, "#16213e",
                20, "#e2d810",
                40, "#ffa500",
                60, "#ffffff",
              ],
              "circle-opacity": 0.5,
            }}
          />
        </Source>
      )}

      {hoveredPort && popupCoords && (
        <Popup
          longitude={popupCoords.lng}
          latitude={popupCoords.lat}
          closeButton={false}
          closeOnClick={false}
          anchor="bottom"
          className="[&_.mapboxgl-popup-content]:bg-card [&_.mapboxgl-popup-content]:text-card-foreground [&_.mapboxgl-popup-content]:border [&_.mapboxgl-popup-content]:border-border [&_.mapboxgl-popup-content]:rounded-lg [&_.mapboxgl-popup-content]:px-3 [&_.mapboxgl-popup-content]:py-2 [&_.mapboxgl-popup-tip]:border-t-card"
        >
          <p className="font-medium text-sm">{hoveredPort.name}</p>
          <p className="text-xs text-muted-foreground">{hoveredPort.country}</p>
        </Popup>
      )}
    </Map>
  );
}
