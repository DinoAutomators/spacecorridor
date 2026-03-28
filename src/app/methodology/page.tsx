import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Footer } from "@/components/layout/footer";

export default function MethodologyPage() {
  return (
    <>
      <div className="mx-auto max-w-4xl px-4 py-12">
        <h1 className="text-3xl font-bold">Methodology</h1>
        <p className="mt-2 text-muted-foreground">
          How SpaceCorridor scores and diagnoses trade corridor decarbonization
          readiness.
        </p>

        <Tabs defaultValue="data" className="mt-8">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="data">Data Sources</TabsTrigger>
            <TabsTrigger value="scoring">Scoring Method</TabsTrigger>
            <TabsTrigger value="bottleneck">Bottleneck Logic</TabsTrigger>
            <TabsTrigger value="limitations">Limitations</TabsTrigger>
          </TabsList>

          <TabsContent value="data" className="mt-6 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">OECD Maritime Transport CO2 Emissions</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-2">
                <p>
                  Emissions baseline data by ship type, route, and country from the OECD
                  Maritime Transport CO2 Emissions Database. Used to establish the carbon
                  intensity of each corridor.
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-base">World Port Index (WPI)</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-2">
                <p>
                  Port coordinates, harbor types, cargo capabilities, and facility data from
                  NGA&apos;s UpdatedPub150.csv. Used to derive services and strategic scores
                  for each port.
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Sentinel-5P OFFL NO2</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-2">
                <p>
                  Tropospheric NO2 column density from Copernicus Sentinel-5P, accessed via
                  Google Earth Engine. Mean NO2 computed within a 25km buffer around each port
                  over a 6-month period. Higher NO2 indicates greater shipping/industrial
                  activity and pollution exposure.
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-base">VIIRS Nighttime Lights</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-2">
                <p>
                  Mean nighttime radiance from NOAA VIIRS DNB Monthly composites via Google
                  Earth Engine. Computed within a 25km buffer around each port. Serves as a
                  proxy for economic activity and port operational intensity.
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="scoring" className="mt-6 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Readiness Score Composition</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                <p className="mb-4">
                  Each corridor receives a composite readiness score (0–100) computed as a
                  weighted average of five sub-scores:
                </p>
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="py-2 font-medium text-foreground">Dimension</th>
                      <th className="py-2 font-medium text-foreground">Weight</th>
                      <th className="py-2 font-medium text-foreground">Source</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    <tr>
                      <td className="py-2">Emissions Score</td>
                      <td className="py-2">25%</td>
                      <td className="py-2">OECD CO2 data</td>
                    </tr>
                    <tr>
                      <td className="py-2">NO2 Score</td>
                      <td className="py-2">20%</td>
                      <td className="py-2">Sentinel-5P</td>
                    </tr>
                    <tr>
                      <td className="py-2">Lights Score</td>
                      <td className="py-2">20%</td>
                      <td className="py-2">VIIRS DNB</td>
                    </tr>
                    <tr>
                      <td className="py-2">Strategic Score</td>
                      <td className="py-2">20%</td>
                      <td className="py-2">WPI port data</td>
                    </tr>
                    <tr>
                      <td className="py-2">Feasibility Score</td>
                      <td className="py-2">15%</td>
                      <td className="py-2">WPI infrastructure</td>
                    </tr>
                  </tbody>
                </table>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Score Interpretation</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-2">
                <p>
                  Higher scores indicate greater readiness for decarbonization. Scores are
                  inverted where necessary — for example, lower NO2 pollution yields a higher
                  NO2 score (cleaner air = more ready).
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full bg-green-500" />
                    <span>70–100: High readiness</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full bg-amber-500" />
                    <span>40–69: Medium readiness</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full bg-red-500" />
                    <span>0–39: Low readiness</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="bottleneck" className="mt-6 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Bottleneck Classification</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-3">
                <p>
                  The bottleneck is determined by identifying the lowest-scoring dimension
                  for each corridor. This reveals the primary barrier to decarbonization:
                </p>
                <ul className="space-y-2 list-disc pl-5">
                  <li>
                    <strong className="text-foreground">Port Infrastructure Gap</strong> —
                    Low feasibility score. Ports lack shore power, LNG bunkering, or modern
                    cargo facilities.
                  </li>
                  <li>
                    <strong className="text-foreground">Fuel Transition Gap</strong> — Low
                    emissions score. High carbon intensity with limited alternative fuel
                    adoption.
                  </li>
                  <li>
                    <strong className="text-foreground">Pollution Exposure Hotspot</strong>{" "}
                    — Low NO2 score. High tropospheric NO2 near ports indicating concentrated
                    emissions.
                  </li>
                  <li>
                    <strong className="text-foreground">
                      Cross-Mode Coordination Gap
                    </strong>{" "}
                    — Low strategic score. Poor intermodal connectivity or limited trade
                    diversification.
                  </li>
                  <li>
                    <strong className="text-foreground">Monitoring/Readiness Gap</strong> —
                    Low lights score. Limited observable economic activity suggesting
                    underdeveloped monitoring infrastructure.
                  </li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="limitations" className="mt-6 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Honest Limitations</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-3">
                <ul className="space-y-2 list-disc pl-5">
                  <li>
                    <strong className="text-foreground">Proxy-based scoring</strong> — NO2
                    and nighttime lights are proxies, not direct measurements of
                    decarbonization readiness.
                  </li>
                  <li>
                    <strong className="text-foreground">Limited corridor sample</strong> —
                    Only 5 corridors analyzed in this prototype. A production system would
                    cover hundreds.
                  </li>
                  <li>
                    <strong className="text-foreground">Static snapshot</strong> — Data
                    represents a recent time period, not live/streaming data.
                  </li>
                  <li>
                    <strong className="text-foreground">Simplified bottleneck logic</strong>{" "}
                    — Rule-based classification from lowest score. Real-world bottlenecks
                    are often multi-dimensional and interrelated.
                  </li>
                  <li>
                    <strong className="text-foreground">No AIS data</strong> — Ship tracking
                    data (AIS) would significantly improve corridor-level emissions
                    estimates but is not included in this prototype.
                  </li>
                  <li>
                    <strong className="text-foreground">OECD data granularity</strong> — OECD
                    emissions are reported at country/ship-type level, not route-level.
                    Country-pair mapping is an approximation.
                  </li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
      <Footer />
    </>
  );
}
