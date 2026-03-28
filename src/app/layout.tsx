import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { Navbar } from "@/components/layout/navbar";
import { TooltipProvider } from "@/components/ui/tooltip";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "SpaceCorridor — Net-Zero Trade Corridor Intelligence",
  description:
    "Diagnose which global trade corridors are most ready for decarbonization using satellite imagery, emissions data, and port intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={cn("min-h-screen bg-background font-sans antialiased", inter.variable)}>
        <TooltipProvider>
          <Navbar />
          <main>{children}</main>
        </TooltipProvider>
      </body>
    </html>
  );
}
