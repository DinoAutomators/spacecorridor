import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Satellite } from "lucide-react";

export function HeroSection() {
  return (
    <section className="relative flex min-h-[80vh] flex-col items-center justify-center px-4 text-center">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-background to-background" />
      <div className="relative z-10 max-w-3xl space-y-6">
        <div className="flex items-center justify-center gap-2 text-blue-400">
          <Satellite className="h-8 w-8" />
        </div>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
          Accelerating{" "}
          <span className="bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            Net-Zero
          </span>{" "}
          Trade Corridors
        </h1>
        <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
          SpaceCorridor diagnoses which global trade corridors are most ready for
          decarbonization — using satellite imagery, emissions data, and port
          intelligence to identify bottlenecks and recommend interventions.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Button asChild size="lg" className="gap-2">
            <Link href="/dashboard">
              Explore Corridors
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/methodology">Our Methodology</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
