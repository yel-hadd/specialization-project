"use client";

import Shell from "@/components/Shell";
import { CardTitle, PageTitle } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { AnomalyReport } from "@/lib/types";

export default function AnomaliesPage() {
  const { t } = useI18n();
  const { data, loading } = useFetch<AnomalyReport>("/analytics/anomalies");

  return (
    <Shell>
      <PageTitle title={t("anomalies.title")} subtitle={t("anomalies.subtitle")} />

      {loading && <p className="text-slate-500">{t("common.analyzing")}</p>}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <CardTitle title={t("anomalies.grades")} info={t("anomalies.grades.info")} />
          <p className="mb-3 text-xs text-slate-500">{t("anomalies.grades.desc")}</p>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-slate-500">
                <th className="py-2">{t("table.student")}</th>
                <th>{t("table.module")}</th>
                <th>{t("table.grade")}</th>
                <th>{t("table.moduleMean")}</th>
                <th>{t("table.zScore")}</th>
              </tr>
            </thead>
            <tbody>
              {data?.grade_outliers.length === 0 && (
                <tr><td colSpan={5} className="py-4 text-slate-400">{t("anomalies.noGrades")}</td></tr>
              )}
              {data?.grade_outliers.map((o, i) => (
                <tr key={i} className="border-b last:border-0">
                  <td className="py-1.5">
                    <a href={`/students/${o.student_id}`} className="text-brand hover:underline">
                      {o.student_code}
                    </a>
                  </td>
                  <td>{o.module_name}</td>
                  <td className={o.value < 10 ? "font-medium text-red-600" : ""}>{o.value}</td>
                  <td>{o.module_mean}</td>
                  <td>{o.z_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <CardTitle title={t("anomalies.absences")} info={t("anomalies.absences.info")} />
          <p className="mb-3 text-xs text-slate-500">{t("anomalies.absences.desc")}</p>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-slate-500">
                <th className="py-2">{t("table.student")}</th>
                <th>{t("table.absenceHours")}</th>
              </tr>
            </thead>
            <tbody>
              {data?.absence_outliers.length === 0 && (
                <tr><td colSpan={2} className="py-4 text-slate-400">{t("anomalies.noAbsences")}</td></tr>
              )}
              {data?.absence_outliers.map((o, i) => (
                <tr key={i} className="border-b last:border-0">
                  <td className="py-1.5">
                    <a href={`/students/${o.student_id}`} className="text-brand hover:underline">
                      {o.student_code}
                    </a>
                  </td>
                  <td>{o.absence_hours} h</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Shell>
  );
}
