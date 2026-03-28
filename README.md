# SpaceCorridor

Geospatial intelligence platform that diagnoses which trade corridors are most ready for decarbonization, identifies bottlenecks, and recommends interventions.

## Quick Start

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui (dark theme)
- **Map**: Mapbox GL JS + react-map-gl
- **Charts**: Recharts (RadarChart, BarChart)
- **Backend**: Supabase (optional — falls back to local JSON data)
- **Data Pipeline**: Python scripts (pandas, geopandas, ee)

## Data Sources

- OECD Maritime Transport CO2 Emissions
- World Port Index (WPI)
- Sentinel-5P OFFL NO2 (Google Earth Engine)
- VIIRS Nighttime Lights (Google Earth Engine)

## Environment Variables

Copy `.env.local` and fill in:

```
NEXT_PUBLIC_MAPBOX_TOKEN=pk.your_token
NEXT_PUBLIC_SUPABASE_URL=your_url        # optional
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key   # optional
```

## Corridors Analyzed

| Corridor | Region | Ports |
|----------|--------|-------|
| Singapore → Rotterdam | Asia-Europe | Singapore, Rotterdam |
| Shanghai → Los Angeles | Trans-Pacific | Shanghai, Los Angeles |
| Jebel Ali → Mumbai | Regional | Jebel Ali, Mumbai (JNPT) |
| Busan → Long Beach | Trans-Pacific | Busan, Long Beach |
| Algeciras → Santos | Atlantic | Algeciras, Santos |
