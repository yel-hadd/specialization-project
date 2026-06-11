"use client";

import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { AnomalyReport } from "@/lib/types";

export default function AnomaliesPage() {
  const { data, loading } = useFetch<AnomalyReport>("/analytics/anomalies");

  return (
    <Shell>
      <PageTitle
        title="Detection d'anomalies"
        subtitle="Notes inhabituelles et absences excessives"
      />

      {loading && <p className="text-slate-500">Analyse en cours...</p>}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-1">Notes inhabituelles</h2>
          <p className="text-xs text-slate-500 mb-3">
            Notes tres eloignees de la moyenne du module (score z &ge; 2.5).
          </p>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b">
                <th className="py-2">Etudiant</th>
                <th>Module</th>
                <th>Note</th>
                <th>Moy. module</th>
                <th>Score z</th>
              </tr>
            </thead>
            <tbody>
              {data?.grade_outliers.length === 0 && (
                <tr><td colSpan={5} className="py-4 text-slate-400">Aucune note anormale.</td></tr>
              )}
              {data?.grade_outliers.map((o, i) => (
                <tr key={i} className="border-b last:border-0">
                  <td className="py-1.5">
                    <a href={`/students/${o.student_id}`} className="text-brand hover:underline">
                      {o.student_code}
                    </a>
                  </td>
                  <td>{o.module_name}</td>
                  <td className={o.value < 10 ? "text-red-600 font-medium" : ""}>{o.value}</td>
                  <td>{o.module_mean}</td>
                  <td>{o.z_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-1">Absences excessives</h2>
          <p className="text-xs text-slate-500 mb-3">
            Etudiants au-dessus du seuil IQR du total d&apos;heures d&apos;absence.
          </p>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b">
                <th className="py-2">Etudiant</th>
                <th>Heures d&apos;absence</th>
              </tr>
            </thead>
            <tbody>
              {data?.absence_outliers.length === 0 && (
                <tr><td colSpan={2} className="py-4 text-slate-400">Aucune absence anormale.</td></tr>
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
