"use client";

import { useParams } from "next/navigation";
import Shell from "@/components/Shell";
import { ProgressionChart } from "@/components/charts";
import { CardTitle, KpiCard, PageTitle, SegmentBadge } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { StudentDetail } from "@/lib/types";

export default function StudentDetailPage() {
  const { t } = useI18n();
  const params = useParams();
  const id = params.id as string;
  const { data, loading } = useFetch<StudentDetail>(`/students/${id}`);
  const modules = useFetch<{ id: number; name: string }[]>("/modules");
  const moduleName = (mid: number) =>
    modules.data?.find((m) => m.id === mid)?.name || `#${mid}`;

  if (loading || !data) {
    return (
      <Shell>
        <p className="text-slate-500">{t("common.loading")}</p>
      </Shell>
    );
  }

  const s = data.student;

  return (
    <Shell>
      <PageTitle
        title={`${s.first_name} ${s.last_name}`}
        subtitle={`${s.student_code} - ${data.class_name || t("student.noClass")}`}
      />

      <div className="mb-6 flex items-center gap-3">
        <span className="text-sm text-slate-500">{t("student.status")} :</span>
        <SegmentBadge segment={data.risk_segment} />
      </div>

      <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        <KpiCard label={t("kpi.average")} value={data.average ?? "-"} hint={t("common.outOf20")} />
        <KpiCard
          label={t("kpi.rank")}
          value={data.rank ? `${data.rank} / ${data.class_size}` : "-"}
          info={t("kpi.rank.info")}
        />
        <KpiCard label={t("kpi.absenceHours")} value={data.absence_hours} />
        <KpiCard
          label={t("kpi.absenceRate")}
          value={`${(data.absence_rate * 100).toFixed(1)}%`}
          info={t("kpi.absenceRate.info")}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <CardTitle title={t("student.evolution")} />
          {data.progression.length > 1 ? (
            <ProgressionChart data={data.progression} />
          ) : (
            <p className="text-sm text-slate-400">{t("student.notEnoughPeriods")}</p>
          )}
        </div>
        <div className="card">
          <CardTitle title={t("student.recommendations")} />
          <ul className="list-disc space-y-1 pl-5 text-sm text-slate-700">
            {data.recommendations.map((r, i) => (
              <li key={i}>{t(`rec.${r}`)}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card mt-6">
        <CardTitle title={t("student.grades", { n: data.grades.length })} />
        <div className="max-h-72 overflow-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="sticky top-0 border-b bg-white text-left text-slate-500">
                <th className="py-2">{t("table.module")}</th>
                <th>{t("table.period")}</th>
                <th>{t("table.grade")}</th>
              </tr>
            </thead>
            <tbody>
              {data.grades.map((g) => (
                <tr key={g.id} className="border-b last:border-0">
                  <td className="py-1.5">{moduleName(g.module_id)}</td>
                  <td>{g.period || "-"}</td>
                  <td className={g.value < 10 ? "font-medium text-red-600" : ""}>{g.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Shell>
  );
}
