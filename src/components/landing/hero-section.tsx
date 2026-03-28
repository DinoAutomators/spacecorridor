"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Satellite, Globe, Ship, BarChart3 } from "lucide-react";

const stats = [
  { value: "20", label: "Trade Corridors" },
  { value: "25+", label: "Major Ports" },
  { value: "4", label: "Satellite Sources" },
  { value: "5", label: "Score Dimensions" },
];

export function HeroSection() {
  return (
    <section className="relative flex min-h-[90vh] flex-col items-center justify-center overflow-hidden px-4 text-center">
      {/* Animated background layers */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/30 via-background to-background" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_right,_var(--tw-gradient-stops))] from-emerald-900/20 via-transparent to-transparent" />

      {/* Dot grid pattern */}
      <div
        className="absolute inset-0 opacity-[0.15]"
        style={{
          backgroundImage: "radial-gradient(circle at 1px 1px, rgba(148,163,184,0.5) 1px, transparent 0)",
          backgroundSize: "40px 40px",
        }}
      />

      {/* Animated orbs */}
      <div className="absolute top-1/4 left-1/4 h-72 w-72 rounded-full bg-blue-500/10 blur-[100px] animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-emerald-500/10 blur-[120px] animate-pulse [animation-delay:1s]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[500px] w-[500px] rounded-full bg-indigo-500/5 blur-[100px] animate-pulse [animation-delay:2s]" />

      {/* Floating icons */}
      <div className="absolute top-[15%] left-[10%] text-blue-500/10 animate-float">
        <Globe className="h-16 w-16" />
      </div>
      <div className="absolute top-[20%] right-[12%] text-emerald-500/10 animate-float [animation-delay:1.5s]">
        <Ship className="h-14 w-14" />
      </div>
      <div className="absolute bottom-[25%] left-[15%] text-indigo-500/10 animate-float [animation-delay:3s]">
        <BarChart3 className="h-12 w-12" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-4xl space-y-8">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-sm text-blue-400 backdrop-blur-sm">
          <Satellite className="h-4 w-4" />
          <span>Powered by Satellite Intelligence</span>
        </div>

        <h1 className="text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
          Accelerating{" "}
          <span className="relative">
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              Net-Zero
            </span>
            <span className="absolute -bottom-1 left-0 right-0 h-px bg-gradient-to-r from-blue-400/0 via-cyan-400/50 to-emerald-400/0" />
          </span>
          <br />
          Trade Corridors
        </h1>

        <p className="mx-auto max-w-2xl text-lg leading-relaxed text-muted-foreground sm:text-xl">
          Diagnose which global trade corridors are most ready for
          decarbonization — using{" "}
          <span className="text-blue-400/90">satellite imagery</span>,{" "}
          <span className="text-emerald-400/90">emissions data</span>, and{" "}
          <span className="text-cyan-400/90">port intelligence</span>{" "}
          to identify bottlenecks and recommend interventions.
        </p>

        <div className="flex items-center justify-center gap-4 pt-2">
          <Button asChild size="lg" className="gap-2 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 border-0 text-white shadow-lg shadow-blue-500/20 transition-all hover:shadow-blue-500/30 hover:scale-105">
            <Link href="/dashboard">
              Explore Corridors
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="border-border/60 hover:border-blue-500/40 hover:bg-blue-500/5 transition-all">
            <Link href="/methodology">Our Methodology</Link>
          </Button>
        </div>
      </div>

      {/* Stats bar */}
      <div className="relative z-10 mt-20 w-full max-w-4xl">
        <div className="rounded-2xl border border-border/40 bg-card/40 p-6 backdrop-blur-md">
          <div className="grid grid-cols-2 gap-6 sm:grid-cols-4">
            {stats.map((stat, i) => (
              <div key={stat.label} className="relative text-center">
                {i > 0 && (
                  <div className="absolute left-0 top-1/2 hidden h-8 w-px -translate-y-1/2 bg-border/40 sm:block" />
                )}
                <div className="text-3xl font-bold bg-gradient-to-b from-foreground to-foreground/60 bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="mt-1 text-xs text-muted-foreground tracking-wide uppercase">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent" />
    </section>
  );
}
