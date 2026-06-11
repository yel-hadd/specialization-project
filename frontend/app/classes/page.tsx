"use client";

import Shell from "@/components/Shell";
import { ClassBarChart } from "@/components/charts";
import { PageTitle } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { ClassStat } from "@/lib/types";

export default function ClassesPage() {
  const { data } = useFetch<ClassStat[]>("/analytics/classes");

  return (
    <Shell>
      <PageTitle title="Analyse par classe" subtitle="Comparaison des performances entre classes" />
      <div className="card mb-6">
        <h2 className="font-semibold mb-3">Moyenne par classe</h2>
        {data && <ClassBarChart data={data} />}
      </div>
      <div className="card">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="py-2">Classe</th>
              <th>Moyenne</th>
              <th>Ecart-type</th>
              <th>Taux de reussite</th>
              <th>Etudiants</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((c) => (
              <tr key={c.class_id} className="border-b last:border-0">
                <td className="py-2 font-medium">{c.class_name}</td>
                <td>{c.mean}</td>
                <td>{c.std}</td>
                <td>{(c.success_rate * 100).toFixed(1)}%</td>
                <td>{c.n_students}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
