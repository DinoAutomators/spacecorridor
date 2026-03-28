import { Satellite, BarChart3, AlertTriangle } from "lucide-react";

const steps = [
  {
    icon: Satellite,
    step: "01",
    title: "Analyze",
    description:
      "Fuse OECD emissions data, World Port Index capabilities, Sentinel-5P NO2 imagery, and VIIRS nighttime lights into corridor-level metrics.",
  },
  {
    icon: BarChart3,
    step: "02",
    title: "Score",
    description:
      "Compute a weighted readiness score across 5 dimensions: emissions baseline, pollution exposure, economic activity, strategic value, and feasibility.",
  },
  {
    icon: AlertTriangle,
    step: "03",
    title: "Diagnose",
    description:
      "Identify the primary bottleneck for each corridor and recommend targeted interventions to accelerate decarbonization.",
  },
];

export function HowItWorksSection() {
  return (
    <section className="border-t border-border/40 bg-card/30 px-4 py-24">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-center text-2xl font-bold sm:text-3xl">
          How It Works
        </h2>
        <div className="mt-12 grid gap-8 sm:grid-cols-3">
          {steps.map((s) => (
            <div key={s.step} className="text-center space-y-4">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/10">
                <s.icon className="h-7 w-7 text-blue-400" />
              </div>
              <div className="text-xs font-bold tracking-widest text-blue-400">
                STEP {s.step}
              </div>
              <h3 className="text-lg font-semibold">{s.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {s.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
