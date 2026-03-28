import Link from "next/link";
import { Satellite } from "lucide-react";

export function Footer() {
  return (
    <footer className="relative border-t border-border/20">
      <div className="absolute inset-0 bg-gradient-to-t from-card/40 to-transparent" />
      <div className="relative mx-auto max-w-7xl px-4 py-10">
        <div className="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
          <div className="flex items-center gap-2">
            <Satellite className="h-5 w-5 text-blue-400" />
            <span className="font-semibold">SpaceCorridor</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <Link href="/dashboard" className="hover:text-foreground transition-colors">
              Dashboard
            </Link>
            <Link href="/methodology" className="hover:text-foreground transition-colors">
              Methodology
            </Link>
          </div>
          <p className="text-xs text-muted-foreground/60">
            Data: OECD &middot; WPI &middot; Sentinel-5P &middot; VIIRS
          </p>
        </div>
      </div>
    </footer>
  );
}
