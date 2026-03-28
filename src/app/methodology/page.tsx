import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Footer } from "@/components/layout/footer";
import {
  Database,
  Satellite,
  Sun,
  Ship,
  BarChart3,
  AlertTriangle,
  Target,
  Lightbulb,
  Scale,
  Building2,
  Fuel,
  Cloud,
  GitBranch,
  Activity,
  Info,
} from "lucide-react";

const dataSources = [
  {
    icon: Ship,
    name: "OECD Maritime Transport CO2 Emissions",
    tag: "Emissions Baseline",
    tagColor: "bg-red-500/10 text-red-400 border-red-500/20",
    description:
      "Emissions baseline data by ship type, route, and country from the OECD Maritime Transport CO2 Emissions Database.",
    usage: "Establishes the carbon intensity of each corridor",
    format: "CSV",
    access: "OECD.Stat portal",
    metric: "CO₂ tonnes per country-pair",
  },
  {
    icon: Database,
    name: "World Port Index (WPI)",
    tag: "Port Intelligence",
    tagColor: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    description:
      "Port coordinates, harbor types, cargo capabilities, and facility data from NGA's UpdatedPub150.csv.",
    usage: "Derives services and strategic scores for each port",
    format: "CSV (UpdatedPub150.csv)",
    access: "NGA Maritime Safety Office",
    metric: "150+ port attributes per entry",
  },
  {
    icon: Satellite,
    name: "Sentinel-5P OFFL NO₂",
    tag: "Satellite Imagery",
    tagColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    description:
      "Tropospheric NO₂ column density from Copernicus Sentinel-5P, accessed via Google Earth Engine.",
    usage:
      "Mean NO₂ computed within a 25km buffer around each port over a 6-month period. Higher NO₂ indicates greater shipping/industrial activity and pollution exposure.",
    format: "GEE ImageCollection",
    access: "COPERNICUS/S5P/OFFL/L3_NO2",
    metric: "µmol/m² (tropospheric column)",
  },
  {
    icon: Sun,
    name: "VIIRS Nighttime Lights",
    tag: "Satellite Imagery",
    tagColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    description:
      "Mean nighttime radiance from NOAA VIIRS DNB Monthly composites via Google Earth Engine.",
    usage:
      "Computed within a 25km buffer around each port. Serves as a proxy for economic activity and port operational intensity.",
    format: "GEE ImageCollection",
    access: "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG",
    metric: "nW/cm²/sr (avg radiance)",
  },
];

const scoringDimensions = [
  {
    name: "Emissions Score",
    weight: 25,
    source: "OECD CO₂ data",
    color: "bg-red-500",
    description:
      "Inverse of corridor carbon intensity. Lower emissions → higher score → more ready for green transition.",
  },
  {
    name: "NO₂ Score",
    weight: 20,
    source: "Sentinel-5P",
    color: "bg-amber-500",
    description:
      "Inverse of tropospheric NO₂ concentration near ports. Cleaner air indicates better existing emission controls.",
  },
  {
    name: "Lights Score",
    weight: 20,
    source: "VIIRS DNB",
    color: "bg-yellow-500",
    description:
      "Nighttime radiance as proxy for economic activity and monitoring infrastructure capacity.",
  },
  {
    name: "Strategic Score",
    weight: 20,
    source: "WPI port data",
    color: "bg-blue-500",
    description:
      "Port-pair strategic importance derived from harbor size, cargo capabilities, and trade connectivity.",
  },
  {
    name: "Feasibility Score",
    weight: 15,
    source: "WPI infrastructure",
    color: "bg-purple-500",
    description:
      "Port infrastructure readiness — fuel services, dry dock, shelter, and existing facility quality.",
  },
];

const bottlenecks = [
  {
    icon: Building2,
    name: "Port Infrastructure Gap",
    trigger: "Lowest: Feasibility Score",
    color: "text-purple-400",
    bgColor: "bg-purple-500/10",
    description:
      "Ports lack shore power, LNG bunkering, or modern cargo facilities needed for green corridor operations.",
  },
  {
    icon: Fuel,
    name: "Fuel Transition Gap",
    trigger: "Lowest: Emissions Score",
    color: "text-red-400",
    bgColor: "bg-red-500/10",
    description:
      "High carbon intensity with limited alternative fuel adoption. Corridor relies heavily on conventional bunker fuels.",
  },
  {
    icon: Cloud,
    name: "Pollution Exposure Hotspot",
    trigger: "Lowest: NO₂ Score",
    color: "text-amber-400",
    bgColor: "bg-amber-500/10",
    description:
      "High tropospheric NO₂ near ports indicating concentrated shipping and industrial emissions requiring ECA designation.",
  },
  {
    icon: GitBranch,
    name: "Cross-Mode Coordination Gap",
    trigger: "Lowest: Strategic Score",
    color: "text-blue-400",
    bgColor: "bg-blue-500/10",
    description:
      "Poor intermodal connectivity or limited trade diversification. Ports lack integration with rail, road, and digital freight systems.",
  },
  {
    icon: Activity,
    name: "Monitoring/Readiness Gap",
    trigger: "Lowest: Lights Score",
    color: "text-yellow-400",
    bgColor: "bg-yellow-500/10",
    description:
      "Limited observable economic activity suggesting underdeveloped monitoring, reporting, and verification (MRV) infrastructure.",
  },
];

const limitations = [
  {
    title: "Proxy-based scoring",
    description:
      "NO₂ and nighttime lights are environmental proxies, not direct measurements of decarbonization readiness. They correlate with but do not deterministically indicate transition capacity.",
  },
  {
    title: "Limited corridor sample",
    description:
      "Only 5 corridors (10 ports) analyzed in this prototype. A production system would cover hundreds of corridors across all major trade lanes.",
  },
  {
    title: "Static snapshot",
    description:
      "Data represents a recent 6-month period, not live or streaming data. Seasonal variations and recent policy changes may not be captured.",
  },
  {
    title: "Simplified bottleneck logic",
    description:
      "Rule-based classification from lowest score dimension. Real-world bottlenecks are often multi-dimensional, interrelated, and context-dependent.",
  },
  {
    title: "No AIS data",
    description:
      "Ship tracking data (AIS) would significantly improve corridor-level emissions estimates with actual vessel counts and speeds, but is not included in this prototype.",
  },
  {
    title: "OECD data granularity",
    description:
      "OECD emissions are reported at country/ship-type level, not route-level. Country-pair mapping to specific corridors is an approximation.",
  },
];

export default function MethodologyPage() {
  return (
    <>
      <div className="mx-auto max-w-5xl px-4 py-12">
        {/* Header */}
        <div className="space-y-3 mb-10">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10">
              <Scale className="h-5 w-5 text-blue-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">Methodology</h1>
              <p className="text-muted-foreground">
                How SpaceCorridor scores and diagnoses trade corridor
                decarbonization readiness
              </p>
            </div>
          </div>
        </div>

        <Tabs defaultValue="data" className="space-y-6">
          <TabsList className="w-full grid grid-cols-4 h-11">
            <TabsTrigger value="data" className="gap-1.5 text-xs sm:text-sm">
              <Database className="h-3.5 w-3.5 hidden sm:block" />
              Data Sources
            </TabsTrigger>
            <TabsTrigger
              value="scoring"
              className="gap-1.5 text-xs sm:text-sm"
            >
              <BarChart3 className="h-3.5 w-3.5 hidden sm:block" />
              Scoring
            </TabsTrigger>
            <TabsTrigger
              value="bottleneck"
              className="gap-1.5 text-xs sm:text-sm"
            >
              <AlertTriangle className="h-3.5 w-3.5 hidden sm:block" />
              Bottlenecks
            </TabsTrigger>
            <TabsTrigger
              value="limitations"
              className="gap-1.5 text-xs sm:text-sm"
            >
              <Info className="h-3.5 w-3.5 hidden sm:block" />
              Limitations
            </TabsTrigger>
          </TabsList>

          {/* DATA SOURCES */}
          <TabsContent value="data" className="space-y-4">
            <div className="rounded-lg border bg-card/50 p-4 mb-6">
              <p className="text-sm text-muted-foreground leading-relaxed">
                SpaceCorridor fuses four independent data sources — maritime
                emissions records, port infrastructure databases, and two
                satellite-derived environmental indicators — to build a
                multi-dimensional view of each corridor&apos;s decarbonization
                landscape.
              </p>
            </div>

            <div className="grid gap-4">
              {dataSources.map((source) => (
                <Card
                  key={source.name}
                  className="group transition-all hover:border-border/80 hover:shadow-md hover:shadow-blue-500/5"
                >
                  <CardContent className="p-5">
                    <div className="flex gap-4">
                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-blue-500/10">
                        <source.icon className="h-5 w-5 text-blue-400" />
                      </div>
                      <div className="space-y-2 min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                          <h3 className="font-semibold text-sm">
                            {source.name}
                          </h3>
                          <Badge
                            variant="outline"
                            className={source.tagColor}
                          >
                            {source.tag}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {source.description}
                        </p>
                        <p className="text-sm leading-relaxed">
                          {source.usage}
                        </p>
                        <Separator className="my-2" />
                        <div className="flex flex-wrap gap-x-6 gap-y-1 text-xs text-muted-foreground">
                          <span>
                            <span className="text-foreground font-medium">
                              Format:
                            </span>{" "}
                            {source.format}
                          </span>
                          <span>
                            <span className="text-foreground font-medium">
                              Access:
                            </span>{" "}
                            {source.access}
                          </span>
                          <span>
                            <span className="text-foreground font-medium">
                              Metric:
                            </span>{" "}
                            {source.metric}
                          </span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* SCORING METHOD */}
          <TabsContent value="scoring" className="space-y-6">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Target className="h-4 w-4 text-blue-400" />
                  Readiness Score Composition
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Each corridor receives a composite readiness score (0–100)
                  computed as a weighted average of five sub-scores. Weights
                  reflect the relative importance of each dimension for
                  actionable decarbonization assessment.
                </p>

                <div className="space-y-3 mt-4">
                  {scoringDimensions.map((dim) => (
                    <div
                      key={dim.name}
                      className="rounded-lg border p-4 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div
                            className={`h-2.5 w-2.5 rounded-full ${dim.color}`}
                          />
                          <span className="font-medium text-sm">
                            {dim.name}
                          </span>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-xs text-muted-foreground">
                            {dim.source}
                          </span>
                          <Badge variant="secondary" className="font-mono">
                            {dim.weight}%
                          </Badge>
                        </div>
                      </div>
                      <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
                        <div
                          className={`h-full rounded-full ${dim.color} transition-all`}
                          style={{ width: `${dim.weight}%` }}
                        />
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {dim.description}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Lightbulb className="h-4 w-4 text-amber-400" />
                  Score Interpretation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Higher scores indicate greater readiness for decarbonization.
                  Scores are inverted where necessary — for example, lower NO₂
                  pollution yields a higher NO₂ score (cleaner air = more
                  ready).
                </p>
                <div className="grid grid-cols-3 gap-3 mt-2">
                  <div className="rounded-lg border border-green-500/20 bg-green-500/5 p-4 text-center space-y-1">
                    <div className="h-3 w-3 rounded-full bg-green-500 mx-auto" />
                    <p className="text-lg font-bold text-green-400">70–100</p>
                    <p className="text-xs text-muted-foreground">
                      High Readiness
                    </p>
                    <p className="text-[10px] text-muted-foreground/70">
                      Strong foundation for green corridor designation
                    </p>
                  </div>
                  <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-4 text-center space-y-1">
                    <div className="h-3 w-3 rounded-full bg-amber-500 mx-auto" />
                    <p className="text-lg font-bold text-amber-400">40–69</p>
                    <p className="text-xs text-muted-foreground">
                      Medium Readiness
                    </p>
                    <p className="text-[10px] text-muted-foreground/70">
                      Targeted interventions can unlock progress
                    </p>
                  </div>
                  <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4 text-center space-y-1">
                    <div className="h-3 w-3 rounded-full bg-red-500 mx-auto" />
                    <p className="text-lg font-bold text-red-400">0–39</p>
                    <p className="text-xs text-muted-foreground">
                      Low Readiness
                    </p>
                    <p className="text-[10px] text-muted-foreground/70">
                      Fundamental infrastructure gaps remain
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Formula */}
            <div className="rounded-lg border bg-muted/30 p-5">
              <p className="text-xs font-medium text-muted-foreground mb-2 uppercase tracking-wider">
                Formula
              </p>
              <code className="text-sm text-foreground">
                Readiness = 0.25(Emissions) + 0.20(NO₂) + 0.20(Lights) +
                0.20(Strategic) + 0.15(Feasibility)
              </code>
            </div>
          </TabsContent>

          {/* BOTTLENECK LOGIC */}
          <TabsContent value="bottleneck" className="space-y-4">
            <div className="rounded-lg border bg-card/50 p-4 mb-2">
              <p className="text-sm text-muted-foreground leading-relaxed">
                The bottleneck is determined by identifying the{" "}
                <span className="text-foreground font-medium">
                  lowest-scoring dimension
                </span>{" "}
                for each corridor. This reveals the primary barrier to
                decarbonization and maps to a specific intervention category.
              </p>
            </div>

            {/* Visual flow */}
            <div className="flex items-center justify-center gap-2 py-3 text-xs text-muted-foreground">
              <div className="rounded border px-3 py-1.5 bg-card">
                5 Sub-scores
              </div>
              <span>→</span>
              <div className="rounded border px-3 py-1.5 bg-card">
                Find Minimum
              </div>
              <span>→</span>
              <div className="rounded border px-3 py-1.5 bg-card">
                Map to Category
              </div>
              <span>→</span>
              <div className="rounded border px-3 py-1.5 bg-blue-500/10 border-blue-500/20 text-blue-400">
                Intervention
              </div>
            </div>

            <div className="grid gap-3">
              {bottlenecks.map((b) => (
                <Card
                  key={b.name}
                  className="group transition-all hover:border-border/80"
                >
                  <CardContent className="p-4">
                    <div className="flex gap-4">
                      <div
                        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${b.bgColor}`}
                      >
                        <b.icon className={`h-5 w-5 ${b.color}`} />
                      </div>
                      <div className="space-y-1 min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                          <h3 className="font-semibold text-sm">{b.name}</h3>
                          <Badge
                            variant="outline"
                            className="text-[10px] font-normal"
                          >
                            {b.trigger}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {b.description}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* LIMITATIONS */}
          <TabsContent value="limitations" className="space-y-4">
            <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-4 mb-2">
              <div className="flex gap-3">
                <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-sm">Honest Limitations</p>
                  <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
                    SpaceCorridor is a hackathon prototype designed to
                    demonstrate the feasibility of satellite-informed corridor
                    diagnostics. The following limitations should be considered
                    when interpreting results.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid gap-3">
              {limitations.map((lim, i) => (
                <div
                  key={lim.title}
                  className="flex gap-4 rounded-lg border p-4"
                >
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-muted text-xs font-mono text-muted-foreground">
                    {i + 1}
                  </div>
                  <div className="space-y-1">
                    <h3 className="font-medium text-sm">{lim.title}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {lim.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <Separator />

            <div className="rounded-lg border bg-card/50 p-4">
              <p className="text-xs text-muted-foreground leading-relaxed">
                Despite these limitations, the approach demonstrates that
                combining open satellite data with maritime databases can produce
                actionable corridor-level diagnostics — a capability that does
                not exist in any single current platform.
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </div>
      <Footer />
    </>
  );
}
