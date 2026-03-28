import { Satellite } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background/50">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-6 text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <Satellite className="h-4 w-4" />
          <span>SpaceCorridor</span>
        </div>
        <p>
          Data: OECD, WPI, Sentinel-5P, VIIRS &middot; Built for Hackathon 2026
        </p>
      </div>
    </footer>
  );
}
