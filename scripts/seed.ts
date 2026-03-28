import { createClient } from "@supabase/supabase-js";
import * as fs from "fs";
import * as path from "path";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("Missing SUPABASE_URL or SUPABASE_ANON_KEY env vars");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

const dataDir = path.resolve(__dirname, "../data/processed");

async function seed() {
  console.log("Reading processed data...");

  const ports = JSON.parse(fs.readFileSync(path.join(dataDir, "ports.json"), "utf-8"));
  const corridors = JSON.parse(fs.readFileSync(path.join(dataDir, "corridors.json"), "utf-8"));
  const scores = JSON.parse(fs.readFileSync(path.join(dataDir, "corridor_scores.json"), "utf-8"));

  console.log(`Seeding ${ports.length} ports...`);
  const { error: portsErr } = await supabase.from("ports").upsert(ports, { onConflict: "id" });
  if (portsErr) {
    console.error("Error seeding ports:", portsErr);
    process.exit(1);
  }

  console.log(`Seeding ${corridors.length} corridors...`);
  const { error: corridorsErr } = await supabase
    .from("corridors")
    .upsert(corridors, { onConflict: "id" });
  if (corridorsErr) {
    console.error("Error seeding corridors:", corridorsErr);
    process.exit(1);
  }

  console.log(`Seeding ${scores.length} corridor scores...`);
  const { error: scoresErr } = await supabase
    .from("corridor_scores")
    .upsert(scores, { onConflict: "id" });
  if (scoresErr) {
    console.error("Error seeding corridor_scores:", scoresErr);
    process.exit(1);
  }

  console.log("Seed complete!");
}

seed().catch((err) => {
  console.error("Seed failed:", err);
  process.exit(1);
});
