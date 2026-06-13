"use client";

import { useState } from "react";
import Shell from "@/components/Shell";
import { DistributionChart, ModuleChart } from "@/components/charts";
import { CardTitle, PageTitle } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { ClassStat, Distribution, ModuleStat } from "@/lib/types";

export default function ModulesPage() {
  const { t } = useI18n();
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
      <PageTitle title={t("modules.title")} subtitle={t("modules.subtitle")} />

      <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <CardTitle title={t("modules.successFail")} info={t("modules.successFail.info")} />
          {data && <ModuleChart data={data} />}
        </div>
        <div className="card">
          <CardTitle title={t("chart.distribution.title")} />
          <div className="mb-3 flex flex-wrap gap-2">
            <select
              className="input w-40"
              value={moduleId ?? ""}
              onChange={(e) => setModuleId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">{t("filter.allModules")}</option>
              {data?.map((m) => (
                <option key={m.module_id} value={m.module_id}>{m.module_name}</option>
              ))}
            </select>
            <select
              className="input w-40"
              value={classId ?? ""}
              onChange={(e) => setClassId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">{t("filter.allClasses")}</option>
              {classes.data?.map((c) => (
                <option key={c.class_id} value={c.class_id}>{c.class_name}</option>
              ))}
            </select>
            <select
              className="input w-36"
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
            >
              <option value="">{t("filter.allPeriods")}</option>
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
            <tr className="border-b text-left text-slate-500">
              <th className="py-2">{t("table.module")}</th>
              <th>{t("table.mean")}</th>
              <th>{t("table.median")}</th>
              <th>{t("table.min")}</th>
              <th>{t("table.max")}</th>
              <th>{t("table.variance")}</th>
              <th>{t("table.std")}</th>
              <th>{t("table.q1")}</th>
              <th>{t("table.q3")}</th>
              <th>{t("table.success")}</th>
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
