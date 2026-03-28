export const MAPBOX_STYLE = "mapbox://styles/mapbox/dark-v11";

export const INITIAL_VIEW_STATE = {
  longitude: 40,
  latitude: 20,
  zoom: 1.8,
  pitch: 0,
  bearing: 0,
};

export const CORRIDOR_LINE_PAINT = {
  "line-width": 3,
  "line-opacity": 0.8,
};

export const PORT_CIRCLE_PAINT = {
  "circle-radius": 7,
  "circle-color": "#60a5fa",
  "circle-stroke-width": 2,
  "circle-stroke-color": "#1e3a5f",
};

export const NO2_HEATMAP_PAINT = {
  "heatmap-weight": ["get", "no2_mean"],
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
};

export const VIIRS_CIRCLE_PAINT = {
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
};
