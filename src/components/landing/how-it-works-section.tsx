import { Satellite, BarChart3, AlertTriangle, ChevronRight } from "lucide-react";

const steps = [
  {
    icon: Satellite,
    step: "01",
    title: "Analyze",
    description:
      "Fuse OECD emissions data, World Port Index capabilities, Sentinel-5P NO\u2082 imagery, and VIIRS nighttime lights into corridor-level metrics.",
    sources: ["OECD CO\u2082", "World Port Index", "Sentinel-5P", "VIIRS DNB"],
    color: "blue",
  },
  {
    icon: BarChart3,
    step: "02",
    title: "Score",
    description:
      "Compute a weighted readiness score across 5 dimensions: emissions baseline, pollution exposure, economic activity, strategic value, and feasibility.",
    sources: ["Emissions", "NO\u2082 Pollution", "Night Lights", "Strategic", "Feasibility"],
    color: "emerald",
  },
  {
    icon: AlertTriangle,
    step: "03",
    title: "Diagnose",
    description:
      "Identify the primary bottleneck for each corridor and recommend targeted interventions to accelerate decarbonization.",
    sources: ["Bottleneck ID", "Risk Rating", "Recommendations", "AI Insights"],
    color: "amber",
  },
];

const colorMap: Record<string, { bg: string; text: string; ring: string; badge: string }> = {
  blue: { bg: "bg-blue-500/10", text: "text-blue-400", ring: "ring-blue-500/20", badge: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
  emerald: { bg: "bg-emerald-500/10", text: "text-emerald-400", ring: "ring-emerald-500/20", badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
  amber: { bg: "bg-amber-500/10", text: "text-amber-400", ring: "ring-amber-500/20", badge: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
};

export function HowItWorksSection() {
  return (
    <section className="relative border-t border-border/20 px-4 py-28">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-card/30 via-background to-background" />
      <div
        className="absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage: "radial-gradient(circle at 1px 1px, rgba(148,163,184,0.4) 1px, transparent 0)",
          backgroundSize: "48px 48px",
        }}
      />

      <div className="relative mx-auto max-w-6xl">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400 mb-4">
            Our Process
          </div>
          <h2 className="text-3xl font-bold sm:text-4xl">
            How{" "}
            <span className="bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              SpaceCorridor
            </span>{" "}
            Works
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground leading-relaxed">
            From raw satellite and emissions data to actionable corridor intelligence in three steps.
          </p>
        </div>

        <div className="mt-16 grid gap-8 sm:grid-cols-3">
          {steps.map((s, i) => {
            const colors = colorMap[s.color];
            return (
              <div key={s.step} className="relative">
                {/* Connector arrow between cards */}
                {i < steps.length - 1 && (
                  <div className="absolute -right-4 top-12 z-10 hidden text-muted-foreground/30 sm:block">
                    <ChevronRight className="h-6 w-6" />
                  </div>
                )}

                <div className="group rounded-xl border border-border/50 bg-card/60 p-6 backdrop-blur-sm transition-all duration-300 hover:border-border hover:-translate-y-1 hover:shadow-xl">
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`flex h-12 w-12 items-center justify-center rounded-lg ${colors.bg} ring-1 ${colors.ring}`}>
                      <s.icon className={`h-6 w-6 ${colors.text}`} />
                    </div>
                    <div>
                      <div className={`text-xs font-bold tracking-widest ${colors.text}`}>
                        STEP {s.step}
                      </div>
                      <h3 className="text-lg font-semibold">{s.title}</h3>
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                    {s.description}
                  </p>

                  {/* Source tags */}
                  <div className="flex flex-wrap gap-1.5">
                    {s.sources.map((src) => (
                      <span
                        key={src}
                        className={`inline-flex items-center rounded-md border px-2 py-0.5 text-[10px] font-medium ${colors.badge}`}
                      >
                        {src}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
