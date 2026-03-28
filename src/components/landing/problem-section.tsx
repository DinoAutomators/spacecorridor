import { Card, CardContent } from "@/components/ui/card";
import { Database, Target, TrendingUp } from "lucide-react";

const problems = [
  {
    icon: Database,
    title: "Fragmented Data",
    description:
      "Emissions, port capabilities, and satellite observations live in separate silos — making corridor-level analysis nearly impossible.",
  },
  {
    icon: Target,
    title: "No Readiness Diagnostics",
    description:
      "Stakeholders lack a systematic way to assess which corridors are closest to decarbonization and what specific gaps remain.",
  },
  {
    icon: TrendingUp,
    title: "Unclear Investment Signals",
    description:
      "Without bottleneck identification, green shipping investments are spread thin instead of targeted where they matter most.",
  },
];

export function ProblemSection() {
  return (
    <section className="mx-auto max-w-5xl px-4 py-24">
      <h2 className="text-center text-2xl font-bold sm:text-3xl">
        The Challenge
      </h2>
      <p className="mx-auto mt-3 max-w-2xl text-center text-muted-foreground">
        Maritime shipping accounts for ~3% of global CO2 emissions. Decarbonizing
        trade corridors requires integrating diverse data sources into actionable
        intelligence.
      </p>
      <div className="mt-12 grid gap-6 sm:grid-cols-3">
        {problems.map((p) => (
          <Card
            key={p.title}
            className="group transition-all hover:border-blue-500/30 hover:shadow-lg hover:shadow-blue-500/5"
          >
            <CardContent className="p-6 space-y-3">
              <p.icon className="h-8 w-8 text-blue-400" />
              <h3 className="font-semibold">{p.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {p.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
