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

  const corridorGeoJSON = useMemo(() => {
    function splitAntimeridian(
      coords: number[][]
    ): GeoJSON.LineString | GeoJSON.MultiLineString {
      const segments: number[][][] = [[]];
      for (let i = 0; i < coords.length; i++) {
        segments[segments.length - 1].push(coords[i]);
        if (i < coords.length - 1) {
          const lngDiff = Math.abs(coords[i + 1][0] - coords[i][0]);
          if (lngDiff > 180) {
            // Crossing the antimeridian — interpolate the break point
            const lng1 = coords[i][0];
            const lat1 = coords[i][1];
            const lng2 = coords[i + 1][0];
            const lat2 = coords[i + 1][1];
            const sign = lng1 > 0 ? 1 : -1;
            const edgeLng = sign * 180;
            const t = (edgeLng - lng1) / (lng2 + sign * 360 - lng1);
            const edgeLat = lat1 + t * (lat2 - lat1);
            segments[segments.length - 1].push([edgeLng, edgeLat]);
            segments.push([[-edgeLng, edgeLat]]);
          }
        }
      }
      if (segments.length === 1) {
        return { type: "LineString", coordinates: segments[0] };
      }
      return {
        type: "MultiLineString",
        coordinates: segments.filter((s) => s.length >= 2),
      };
    }

    return {
      type: "FeatureCollection" as const,
      features: corridors.map((c) => {
        let geometry = c.geometry;
        if (geometry.type === "LineString") {
          geometry = splitAntimeridian(geometry.coordinates);
        }
        return {
          type: "Feature" as const,
          id: c.id,
          properties: {
            id: c.id,
            name: c.name,
            readiness: c.score?.readiness_score ?? 0,
            color: getReadinessColor(c.score?.readiness_score ?? 0),
            selected: c.id === selectedCorridorId ? 1 : 0,
          },
          geometry,
        };
      }),
    };
  }, [corridors, selectedCorridorId]);

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
          const geo = corridor.geometry;
          const flatCoords =
            geo.type === "MultiLineString"
              ? geo.coordinates.flat()
              : geo.coordinates;
          const midIdx = Math.floor(flatCoords.length / 2);
          mapRef.current.flyTo({
            center: [flatCoords[midIdx][0] as number, flatCoords[midIdx][1] as number],
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
