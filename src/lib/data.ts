import { Port, Corridor, CorridorScore } from "@/types";
import path from "path";
import fs from "fs";

const DATA_DIR = path.join(process.cwd(), "data", "processed");

function readJSON<T>(filename: string): T {
  const filePath = path.join(DATA_DIR, filename);
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function hasSupabase(): boolean {
  return !!(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY &&
    process.env.NEXT_PUBLIC_SUPABASE_URL !== "your_supabase_url_here"
  );
}

export async function fetchData(): Promise<{
  ports: Port[];
  corridors: Corridor[];
  scores: CorridorScore[];
}> {
  if (hasSupabase()) {
    const { createClient } = await import("@/lib/supabase/server");
    const supabase = await createClient();

    const [portsRes, corridorsRes, scoresRes] = await Promise.all([
      supabase.from("ports").select("*"),
      supabase.from("corridors").select("*"),
      supabase.from("corridor_scores").select("*"),
    ]);

    return {
      ports: portsRes.data ?? [],
      corridors: corridorsRes.data ?? [],
      scores: scoresRes.data ?? [],
    };
  }

  // Fallback: read from local JSON files
  return {
    ports: readJSON<Port[]>("ports.json"),
    corridors: readJSON<Corridor[]>("corridors.json"),
    scores: readJSON<CorridorScore[]>("corridor_scores.json"),
  };
}
