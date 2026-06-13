"use client";

import Shell from "@/components/Shell";
import { ClassBarChart, CorrelationHeatmap, DistributionChart, SegmentPie } from "@/components/charts";
import { CardTitle, KpiCard, PageTitle } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { ClassStat, CorrelationMatrix, Distribution, Kpis } from "@/lib/types";

export default function DashboardPage() {
  const { t } = useI18n();
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
      <PageTitle title={t("dashboard.title")} subtitle={t("dashboard.subtitle")} />

      <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
        <KpiCard label={t("kpi.students")} value={k?.n_students ?? "-"} />
        <KpiCard
          label={t("kpi.overallAverage")}
          value={k?.overall_average ?? "-"}
          hint={t("common.outOf20")}
          info={t("kpi.overallAverage.info")}
        />
        <KpiCard label={t("kpi.successRate")} value={pct(k?.success_rate)} info={t("kpi.successRate.info")} />
        <KpiCard label={t("kpi.absenceRate")} value={pct(k?.absence_rate)} info={t("kpi.absenceRate.info")} />
        <KpiCard label={t("kpi.atRisk")} value={k?.n_at_risk ?? "-"} info={t("kpi.atRisk.info")} />
        <KpiCard
          label={t("kpi.progression")}
          value={
            k?.progression === null || k?.progression === undefined
              ? "-"
              : `${k.progression > 0 ? "+" : ""}${k.progression} ${t("kpi.progression.unit")}`
          }
          hint={t("kpi.progression.hint")}
          info={t("kpi.progression.info")}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <CardTitle title={t("chart.distribution.title")} />
          {dist.data && <DistributionChart data={dist.data} />}
        </div>
        <div className="card">
          <CardTitle title={t("chart.classMean.title")} />
          {classes.data && <ClassBarChart data={classes.data} />}
        </div>
        <div className="card">
          <CardTitle title={t("chart.correlations.title")} info={t("chart.correlations.info")} />
          {corr.data && <CorrelationHeatmap data={corr.data} />}
          <p className="mt-3 text-xs text-slate-500">{t("chart.correlations.note")}</p>
        </div>
        <div className="card">
          <CardTitle title={t("chart.segments.title")} info={t("chart.segments.info")} />
          {segData.length > 0 && <SegmentPie data={segData} />}
        </div>
      </div>
    </Shell>
  );
}
