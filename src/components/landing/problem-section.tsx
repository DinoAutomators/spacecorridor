import { Database, Target, TrendingUp } from "lucide-react";

const problems = [
  {
    icon: Database,
    title: "Fragmented Data",
    description:
      "Emissions, port capabilities, and satellite observations live in separate silos — making corridor-level analysis nearly impossible.",
    gradient: "from-blue-500 to-cyan-500",
    glow: "group-hover:shadow-blue-500/20",
    iconBg: "bg-blue-500/10",
    iconColor: "text-blue-400",
  },
  {
    icon: Target,
    title: "No Readiness Diagnostics",
    description:
      "Stakeholders lack a systematic way to assess which corridors are closest to decarbonization and what specific gaps remain.",
    gradient: "from-emerald-500 to-teal-500",
    glow: "group-hover:shadow-emerald-500/20",
    iconBg: "bg-emerald-500/10",
    iconColor: "text-emerald-400",
  },
  {
    icon: TrendingUp,
    title: "Unclear Investment Signals",
    description:
      "Without bottleneck identification, green shipping investments are spread thin instead of targeted where they matter most.",
    gradient: "from-amber-500 to-orange-500",
    glow: "group-hover:shadow-amber-500/20",
    iconBg: "bg-amber-500/10",
    iconColor: "text-amber-400",
  },
];

export function ProblemSection() {
  return (
    <section className="relative mx-auto max-w-6xl px-4 py-28">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/5 via-transparent to-transparent" />

      <div className="relative">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1 text-xs font-medium text-red-400 mb-4">
            The Problem
          </div>
          <h2 className="text-3xl font-bold sm:text-4xl">
            The Challenge of{" "}
            <span className="bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              Maritime Decarbonization
            </span>
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground leading-relaxed">
            Maritime shipping accounts for ~3% of global CO&#8322; emissions. Decarbonizing
            trade corridors requires integrating diverse data sources into actionable
            intelligence.
          </p>
        </div>

        <div className="mt-16 grid gap-6 sm:grid-cols-3">
          {problems.map((p) => (
            <div
              key={p.title}
              className={`group relative rounded-xl border border-border/50 bg-card/60 p-6 backdrop-blur-sm transition-all duration-300 hover:border-border hover:-translate-y-1 hover:shadow-xl ${p.glow}`}
            >
              {/* Gradient top accent */}
              <div className={`absolute inset-x-0 top-0 h-px bg-gradient-to-r ${p.gradient} opacity-0 transition-opacity group-hover:opacity-100`} />

              <div className={`inline-flex h-12 w-12 items-center justify-center rounded-lg ${p.iconBg} mb-4`}>
                <p.icon className={`h-6 w-6 ${p.iconColor}`} />
              </div>
              <h3 className="text-lg font-semibold mb-2">{p.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {p.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
