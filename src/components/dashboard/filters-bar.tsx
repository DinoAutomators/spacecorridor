"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Filters } from "@/types";
import { REGIONS, BOTTLENECK_CATEGORIES } from "@/lib/constants";
import { Cloud, Sun } from "lucide-react";

interface FiltersBarProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}

export function FiltersBar({ filters, onFiltersChange }: FiltersBarProps) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <Select
        value={filters.region ?? "all"}
        onValueChange={(v) =>
          onFiltersChange({ ...filters, region: v === "all" ? null : v })
        }
      >
        <SelectTrigger className="w-[150px] h-8 text-xs">
          <SelectValue placeholder="Region" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Regions</SelectItem>
          {REGIONS.map((r) => (
            <SelectItem key={r} value={r}>{r}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        value={filters.bottleneck ?? "all"}
        onValueChange={(v) =>
          onFiltersChange({ ...filters, bottleneck: v === "all" ? null : v })
        }
      >
        <SelectTrigger className="w-[200px] h-8 text-xs">
          <SelectValue placeholder="Bottleneck" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Bottlenecks</SelectItem>
          {BOTTLENECK_CATEGORIES.map((b) => (
            <SelectItem key={b} value={b}>{b}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      <div className="flex items-center gap-2">
        <span className="text-xs text-muted-foreground">Readiness:</span>
        <Slider
          min={0}
          max={100}
          step={1}
          value={[filters.readinessRange[0], filters.readinessRange[1]]}
          onValueChange={(v) =>
            onFiltersChange({
              ...filters,
              readinessRange: [v[0], v[1]],
            })
          }
          className="w-[140px]"
        />
        <span className="text-xs text-muted-foreground tabular-nums w-16">
          {filters.readinessRange[0]}–{filters.readinessRange[1]}
        </span>
      </div>

      <div className="ml-auto flex items-center gap-1">
        <Button
          variant={filters.showNO2Layer ? "default" : "outline"}
          size="sm"
          className="h-7 text-xs gap-1"
          onClick={() =>
            onFiltersChange({ ...filters, showNO2Layer: !filters.showNO2Layer })
          }
        >
          <Cloud className="h-3 w-3" />
          NO2
        </Button>
        <Button
          variant={filters.showLightsLayer ? "default" : "outline"}
          size="sm"
          className="h-7 text-xs gap-1"
          onClick={() =>
            onFiltersChange({
              ...filters,
              showLightsLayer: !filters.showLightsLayer,
            })
          }
        >
          <Sun className="h-3 w-3" />
          Lights
        </Button>
      </div>
    </div>
  );
}
