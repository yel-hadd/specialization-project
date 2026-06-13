"use client";

import { useState } from "react";
import Shell from "@/components/Shell";
import { CardTitle, InfoTip, PageTitle, SegmentBadge, SeverityBadge } from "@/components/ui";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { Alert, AtRiskStudent } from "@/lib/types";

export default function AlertsPage() {
  const { t } = useI18n();
  const [refresh, setRefresh] = useState(0);
  // Bump `refresh` to vary the `_` query param and force a refetch after generating alerts.
  const alerts = useFetch<Alert[]>(`/alerts?_=${refresh}`);
  const atRisk = useFetch<AtRiskStudent[]>(`/analytics/at-risk?_=${refresh}`);
  const [generating, setGenerating] = useState(false);

  async function generate() {
    setGenerating(true);
    try {
      await api.post("/alerts/generate");
      setRefresh((r) => r + 1);
    } finally {
      setGenerating(false);
    }
  }

  // Render the alert message from its structured fields, in the active language.
  function alertMessage(a: Alert): string {
    if (a.alert_type === "low_average") {
      return t("alertMsg.low_average", {
        value: a.metric_value ?? "",
        threshold: a.threshold_value ?? "",
      });
    }
    if (a.alert_type === "high_absence") {
      return t("alertMsg.high_absence", {
        value: a.metric_value != null ? (a.metric_value * 100).toFixed(1) : "",
      });
    }
    if (a.alert_type === "performance_drop") {
      return t("alertMsg.performance_drop", { value: a.metric_value ?? "" });
    }
    return a.message;
  }

  return (
    <Shell>
      <div className="flex items-center justify-between">
        <PageTitle title={t("alerts.title")} subtitle={t("alerts.subtitle")} />
        <div className="flex items-center">
          <button className="btn" onClick={generate} disabled={generating}>
            {generating ? t("alerts.generating") : t("alerts.generate")}
          </button>
          <InfoTip text={t("alerts.generate.info")} />
        </div>
      </div>

      <div className="card mb-6">
        <CardTitle title={t("alerts.active")} />
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left text-slate-500">
              <th className="py-2">{t("table.type")}</th>
              <th>{t("table.severity")}</th>
              <th>{t("table.message")}</th>
              <th>{t("table.student")}</th>
            </tr>
          </thead>
          <tbody>
            {alerts.data?.length === 0 && (
              <tr>
                <td colSpan={4} className="py-4 text-slate-400">{t("alerts.empty")}</td>
              </tr>
            )}
            {alerts.data?.map((a) => (
              <tr key={a.id} className="border-b last:border-0">
                <td className="py-2 font-medium">{t(`alertType.${a.alert_type}`)}</td>
                <td><SeverityBadge severity={a.severity} /></td>
                <td className="text-slate-600">{alertMessage(a)}</td>
                <td>
                  <a href={`/students/${a.student_id}`} className="text-brand hover:underline">
                    #{a.student_id}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <CardTitle title={t("alerts.toFollow")} />
        <div className="space-y-3">
          {atRisk.data?.slice(0, 20).map((s) => (
            <div key={s.student_id} className="rounded-lg border border-slate-100 p-3">
              <div className="flex items-center justify-between">
                <div>
                  <a href={`/students/${s.student_id}`} className="font-medium text-brand hover:underline">
                    {s.name}
                  </a>
                  <span className="ml-2 text-xs text-slate-400">
                    {t("alerts.studentMeta", {
                      class: s.class_name || "-",
                      average: s.average,
                      score: s.risk_score,
                    })}
                  </span>
                </div>
                <SegmentBadge segment={s.segment} />
              </div>
              <ul className="mt-2 list-disc pl-5 text-sm text-slate-600">
                {s.recommendations.map((r, i) => (
                  <li key={i}>{t(`rec.${r}`)}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </Shell>
  );
}
