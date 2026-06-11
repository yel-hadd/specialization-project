"use client";

import Shell from "@/components/Shell";
import { ClassBarChart, CorrelationHeatmap, DistributionChart, SegmentPie } from "@/components/charts";
import { KpiCard, PageTitle } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { ClassStat, CorrelationMatrix, Distribution, Kpis } from "@/lib/types";

export default function DashboardPage() {
  const kpis = useFetch<Kpis>("/analytics/kpis");
  const dist = useFetch<Distribution>("/analytics/distribution");
  const classes = useFetch<ClassStat[]>("/analytics/classes");
  const corr = useFetch<CorrelationMatrix>("/analytics/correlations");
  const seg = useFetch<{ counts: Record<string, number> }>("/analytics/segmentation");

  const k = kpis.data;
  const pct = (v: number | null | undefined) =>
    v === null || v === undefined ? "-" : `${(v * 100).toFixed(1)}%`;

  const segData = seg.data
    ? Object.entries(seg.data.counts).map(([label, size]) => ({ label, size }))
    : [];

  return (
    <Shell>
      <PageTitle title="Tableau de bord pedagogique" subtitle="Vue globale de la performance" />

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        <KpiCard label="Etudiants" value={k?.n_students ?? "-"} />
        <KpiCard label="Moyenne generale" value={k?.overall_average ?? "-"} hint="sur 20" />
        <KpiCard label="Taux de reussite" value={pct(k?.success_rate)} />
        <KpiCard label="Taux d'absence" value={pct(k?.absence_rate)} />
        <KpiCard label="Etudiants a risque" value={k?.n_at_risk ?? "-"} />
        <KpiCard
          label="Progression globale"
          value={
            k?.progression === null || k?.progression === undefined
              ? "-"
              : `${k.progression > 0 ? "+" : ""}${k.progression} pts`
          }
          hint="S1 vers S2"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Distribution des notes</h2>
          {dist.data && <DistributionChart data={dist.data} />}
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Moyenne par classe</h2>
          {classes.data && <ClassBarChart data={classes.data} />}
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Correlations (absences / notes)</h2>
          {corr.data && <CorrelationHeatmap data={corr.data} />}
          <p className="mt-3 text-xs text-slate-500">
            Valeurs negatives entre absences et moyenne: plus d&apos;absences est associe a une moyenne plus basse.
          </p>
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Repartition par segment</h2>
          {segData.length > 0 && <SegmentPie data={segData} />}
        </div>
      </div>
    </Shell>
  );
}
