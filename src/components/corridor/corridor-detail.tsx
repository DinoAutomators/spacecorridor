"use client";

import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CorridorWithDetails } from "@/types";
import { getReadinessColor, getReadinessLabel } from "@/lib/constants";
import { ScoreRadar } from "./score-radar";
import { ScoreBarChart } from "./score-bar-chart";
import { BottleneckCard } from "./bottleneck-card";
import { RecommendationCard } from "./recommendation-card";
import { MapPin } from "lucide-react";

interface CorridorDetailProps {
  corridor: CorridorWithDetails | null;
  open: boolean;
  onClose: () => void;
}

export function CorridorDetail({ corridor, open, onClose }: CorridorDetailProps) {
  if (!corridor || !corridor.score) return null;

  const { score } = corridor;
  const readiness = score.readiness_score;
  const color = getReadinessColor(readiness);

  return (
    <Sheet open={open} onOpenChange={(o) => !o && onClose()}>
      <SheetContent className="w-full sm:max-w-lg overflow-y-auto">
        <SheetHeader>
          <SheetTitle className="text-lg">{corridor.name}</SheetTitle>
          <SheetDescription className="flex items-center gap-2">
            <Badge variant="outline">{corridor.region}</Badge>
            <span
              className="inline-flex items-center gap-1 font-semibold"
              style={{ color }}
            >
              {readiness} — {getReadinessLabel(readiness)}
            </span>
          </SheetDescription>
        </SheetHeader>

        <div className="mt-4 space-y-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <MapPin className="h-3.5 w-3.5" />
            <span>
              {corridor.from_port?.name}, {corridor.from_port?.country}
            </span>
            <span>→</span>
            <span>
              {corridor.to_port?.name}, {corridor.to_port?.country}
            </span>
          </div>

          {corridor.description && (
            <p className="text-sm text-muted-foreground">{corridor.description}</p>
          )}

          <Separator />

          <Tabs defaultValue="radar">
            <TabsList className="w-full">
              <TabsTrigger value="radar" className="flex-1">Radar</TabsTrigger>
              <TabsTrigger value="bar" className="flex-1">Bar Chart</TabsTrigger>
            </TabsList>
            <TabsContent value="radar">
              <ScoreRadar score={score} />
            </TabsContent>
            <TabsContent value="bar">
              <ScoreBarChart score={score} />
            </TabsContent>
          </Tabs>

          <Separator />

          <BottleneckCard bottleneck={score.bottleneck} scores={score} />
          <RecommendationCard recommendation={score.recommendation} />

          {score.ai_explanation && (
            <>
              <Separator />
              <div>
                <h4 className="text-sm font-medium mb-2">AI Analysis</h4>
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {score.ai_explanation}
                </p>
              </div>
            </>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}
