import { DashboardShell } from "@/components/dashboard/dashboard-shell";
import { CorridorWithDetails } from "@/types";
import { fetchData } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const { ports, corridors, scores } = await fetchData();

  const corridorsWithDetails: CorridorWithDetails[] = corridors.map((c) => ({
    ...c,
    from_port: ports.find((p) => p.id === c.from_port_id)!,
    to_port: ports.find((p) => p.id === c.to_port_id)!,
    score: scores.find((s) => s.corridor_id === c.id),
  }));

  return <DashboardShell corridors={corridorsWithDetails} ports={ports} />;
}
