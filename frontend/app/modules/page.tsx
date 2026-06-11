"use client";

import { useState } from "react";
import Shell from "@/components/Shell";
import { DistributionChart, ModuleChart } from "@/components/charts";
import { PageTitle } from "@/components/ui";
import { useFetch } from "@/lib/useApi";
import type { ClassStat, Distribution, ModuleStat } from "@/lib/types";

export default function ModulesPage() {
  const { data } = useFetch<ModuleStat[]>("/analytics/modules");
  const classes = useFetch<ClassStat[]>("/analytics/classes");
  const periods = useFetch<string[]>("/analytics/periods");

  const [moduleId, setModuleId] = useState<number | null>(null);
  const [classId, setClassId] = useState<number | null>(null);
  const [period, setPeriod] = useState<string>("");

  const params = new URLSearchParams();
  if (moduleId) params.set("module_id", String(moduleId));
  if (classId) params.set("class_id", String(classId));
  if (period) params.set("period", period);
  const qs = params.toString();
  const dist = useFetch<Distribution>(
    qs ? `/analytics/distribution?${qs}` : "/analytics/distribution"
  );

  return (
    <Shell>
      <PageTitle title="Analyse par module" subtitle="Modules les plus reussis et les plus difficiles" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="card">
          <h2 className="font-semibold mb-3">Taux de reussite / echec par module</h2>
          {data && <ModuleChart data={data} />}
        </div>
        <div className="card">
          <h2 className="font-semibold mb-3">Distribution des notes</h2>
          <div className="flex flex-wrap gap-2 mb-3">
            <select
              className="input w-40"
              value={moduleId ?? ""}
              onChange={(e) => setModuleId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">Tous les modules</option>
              {data?.map((m) => (
                <option key={m.module_id} value={m.module_id}>{m.module_name}</option>
              ))}
            </select>
            <select
              className="input w-40"
              value={classId ?? ""}
              onChange={(e) => setClassId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">Toutes les classes</option>
              {classes.data?.map((c) => (
                <option key={c.class_id} value={c.class_id}>{c.class_name}</option>
              ))}
            </select>
            <select
              className="input w-36"
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
            >
              <option value="">Toutes les periodes</option>
              {periods.data?.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          {dist.data && <DistributionChart data={dist.data} />}
        </div>
      </div>

      <div className="card">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="py-2">Module</th>
              <th>Moyenne</th>
              <th>Mediane</th>
              <th>Min</th>
              <th>Max</th>
              <th>Variance</th>
              <th>Ecart-type</th>
              <th>Q1</th>
              <th>Q3</th>
              <th>Reussite</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((m) => (
              <tr key={m.module_id} className="border-b last:border-0">
                <td className="py-2 font-medium">{m.module_name}</td>
                <td>{m.mean}</td>
                <td>{m.median}</td>
                <td>{m.min}</td>
                <td>{m.max}</td>
                <td>{m.variance}</td>
                <td>{m.std}</td>
                <td>{m.q1}</td>
                <td>{m.q3}</td>
                <td>{(m.success_rate * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
