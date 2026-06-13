"use client";

import Shell from "@/components/Shell";
import { ClassBarChart } from "@/components/charts";
import { CardTitle, PageTitle } from "@/components/ui";
import { useI18n } from "@/lib/i18n";
import { useFetch } from "@/lib/useApi";
import type { ClassStat } from "@/lib/types";

export default function ClassesPage() {
  const { t } = useI18n();
  const { data } = useFetch<ClassStat[]>("/analytics/classes");

  return (
    <Shell>
      <PageTitle title={t("classes.title")} subtitle={t("classes.subtitle")} />
      <div className="card mb-6">
        <CardTitle title={t("chart.classMean.title")} />
        {data && <ClassBarChart data={data} />}
      </div>
      <div className="card">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left text-slate-500">
              <th className="py-2">{t("table.class")}</th>
              <th>{t("table.mean")}</th>
              <th>{t("table.std")}</th>
              <th>{t("table.successRate")}</th>
              <th>{t("table.students")}</th>
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
