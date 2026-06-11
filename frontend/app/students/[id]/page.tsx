"use client";

import { useParams } from "next/navigation";
import Shell from "@/components/Shell";
import { ProgressionChart } from "@/components/charts";
import { KpiCard, PageTitle, SegmentBadge } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { StudentDetail } from "@/lib/types";

export default function StudentDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const { data, loading } = useFetch<StudentDetail>(`/students/${id}`);
  const modules = useFetch<{ id: number; name: string }[]>("/modules");
  const moduleName = (mid: number) =>
    modules.data?.find((m) => m.id === mid)?.name || `#${mid}`;

  if (loading || !data) {
    return (
      <Shell>
        <p className="text-slate-500">Chargement...</p>
      </Shell>
    );
  }

  const s = data.student;

  return (
    <Shell>
      <PageTitle
        title={`${s.first_name} ${s.last_name}`}
        subtitle={`${s.student_code} - ${data.class_name || "Sans classe"}`}
      />

      <div className="flex items-center gap-3 mb-6">
        <span className="text-sm text-slate-500">Statut:</span>
        <SegmentBadge segment={data.risk_segment} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <KpiCard label="Moyenne" value={data.average ?? "-"} hint="sur 20" />
        <KpiCard
          label="Classement"
          value={data.rank ? `${data.rank} / ${data.class_size}` : "-"}
        />
        <KpiCard label="Heures d'absence" value={data.absence_hours} />
        <KpiCard label="Taux d'absence" value={`${(data.absence_rate * 100).toFixed(1)}%`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Evolution par periode</h2>
          {data.progression.length > 1 ? (
            <ProgressionChart data={data.progression} />
          ) : (
            <p className="text-sm text-slate-400">Pas assez de periodes pour tracer une evolution.</p>
          )}
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Recommandations</h2>
          <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
            {data.recommendations.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card mt-6">
        <h2 className="font-semibold mb-3">Notes ({data.grades.length})</h2>
        <div className="max-h-72 overflow-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b sticky top-0 bg-white">
                <th className="py-2">Module</th>
                <th>Periode</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {data.grades.map((g) => (
                <tr key={g.id} className="border-b last:border-0">
                  <td className="py-1.5">{moduleName(g.module_id)}</td>
                  <td>{g.period || "-"}</td>
                  <td className={g.value < 10 ? "text-red-600 font-medium" : ""}>{g.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Shell>
  );
}
