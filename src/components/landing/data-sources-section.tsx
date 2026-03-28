import { Satellite, Ship, Factory, Lightbulb } from "lucide-react";

const sources = [
  {
    icon: Factory,
    name: "OECD Maritime CO\u2082",
    description: "International emissions baselines by ship type and trade route",
    color: "text-red-400",
    bg: "bg-red-500/10",
  },
  {
    icon: Ship,
    name: "World Port Index",
    description: "Port capabilities, harbor infrastructure, and service levels",
    color: "text-blue-400",
    bg: "bg-blue-500/10",
  },
  {
    icon: Satellite,
    name: "Sentinel-5P NO\u2082",
    description: "Tropospheric nitrogen dioxide concentrations around ports",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
  },
  {
    icon: Lightbulb,
    name: "VIIRS Nighttime Lights",
    description: "Port economic activity proxy from nighttime radiance data",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
  },
];

export function DataSourcesSection() {
  return (
    <section className="relative border-t border-border/20 px-4 py-28">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-emerald-900/10 via-transparent to-transparent" />

      <div className="relative mx-auto max-w-6xl">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400 mb-4">
            Real Data
          </div>
          <h2 className="text-3xl font-bold sm:text-4xl">
            Built on{" "}
            <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Authoritative Sources
            </span>
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground leading-relaxed">
            Every score is derived from real-world observations — no mock data, no estimates.
          </p>
        </div>

        <div className="mt-16 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {sources.map((s) => (
            <div
              key={s.name}
              className="group relative rounded-xl border border-border/50 bg-card/60 p-5 backdrop-blur-sm transition-all duration-300 hover:border-border hover:-translate-y-1"
            >
              <div className={`inline-flex h-10 w-10 items-center justify-center rounded-lg ${s.bg} mb-3`}>
                <s.icon className={`h-5 w-5 ${s.color}`} />
              </div>
              <h3 className="font-semibold text-sm mb-1">{s.name}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {s.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
