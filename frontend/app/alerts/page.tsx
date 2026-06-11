"use client";

import { useState } from "react";
import Shell from "@/components/Shell";
import { PageTitle, SegmentBadge, SeverityBadge } from "@/components/ui";
import { api } from "@/lib/api";
import { useFetch } from "@/lib/useApi";
import type { Alert, AtRiskStudent } from "@/lib/types";

const TYPE_LABELS: Record<string, string> = {
  low_average: "Moyenne faible",
  high_absence: "Absences elevees",
  performance_drop: "Baisse de performance",
};

export default function AlertsPage() {
  const [refresh, setRefresh] = useState(0);
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

  return (
    <Shell>
      <div className="flex items-center justify-between">
        <PageTitle title="Alertes pedagogiques" subtitle="Detection automatique des etudiants a risque" />
        <button className="btn" onClick={generate} disabled={generating}>
          {generating ? "Generation..." : "Generer les alertes"}
        </button>
      </div>

      <div className="card mb-6">
        <h2 className="font-semibold mb-3">Alertes actives</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="py-2">Type</th>
              <th>Gravite</th>
              <th>Message</th>
              <th>Etudiant</th>
            </tr>
          </thead>
          <tbody>
            {alerts.data?.length === 0 && (
              <tr>
                <td colSpan={4} className="py-4 text-slate-400">
                  Aucune alerte. Cliquez sur &quot;Generer les alertes&quot;.
                </td>
              </tr>
            )}
            {alerts.data?.map((a) => (
              <tr key={a.id} className="border-b last:border-0">
                <td className="py-2 font-medium">{TYPE_LABELS[a.alert_type] || a.alert_type}</td>
                <td><SeverityBadge severity={a.severity} /></td>
                <td className="text-slate-600">{a.message}</td>
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
        <h2 className="font-semibold mb-3">Etudiants a suivre et recommandations</h2>
        <div className="space-y-3">
          {atRisk.data?.slice(0, 20).map((s) => (
            <div key={s.student_id} className="border border-slate-100 rounded-lg p-3">
              <div className="flex items-center justify-between">
                <div>
                  <a href={`/students/${s.student_id}`} className="font-medium text-brand hover:underline">
                    {s.name}
                  </a>
                  <span className="ml-2 text-xs text-slate-400">
                    {s.class_name || "-"} | moyenne {s.average} | score {s.risk_score}
                  </span>
                </div>
                <SegmentBadge segment={s.segment} />
              </div>
              <ul className="mt-2 list-disc pl-5 text-sm text-slate-600">
                {s.recommendations.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </Shell>
  );
}
