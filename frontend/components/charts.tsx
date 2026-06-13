"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useI18n } from "@/lib/i18n";
import type {
  ClassStat,
  CorrelationMatrix,
  Distribution,
  ModuleStat,
} from "@/lib/types";

const COLORS = ["#1d4ed8", "#0e9488", "#f59e0b", "#db2777", "#7c3aed", "#dc2626"];

export function DistributionChart({ data }: { data: Distribution }) {
  const { t } = useI18n();
  const rows = data.edges.map((e, i) => ({ tranche: e, count: data.counts[i] }));
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={rows}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="tranche" tick={{ fontSize: 10 }} interval={0} angle={-45} textAnchor="end" height={50} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Bar dataKey="count" name={t("chart.series.grades")} fill="#1d4ed8" radius={[3, 3, 0, 0]} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ClassBarChart({ data }: { data: ClassStat[] }) {
  const { t } = useI18n();
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="class_name" tick={{ fontSize: 11 }} />
        <YAxis domain={[0, 20]} tick={{ fontSize: 11 }} />
        <Tooltip />
        <Bar dataKey="mean" name={t("chart.series.mean")} fill="#0e9488" radius={[3, 3, 0, 0]} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ModuleChart({ data }: { data: ModuleStat[] }) {
  const { t } = useI18n();
  const rows = data.map((m) => ({
    name: m.module_name,
    reussite: Math.round(m.success_rate * 100),
    echec: Math.round(m.fail_rate * 100),
  }));
  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={rows} layout="vertical" margin={{ left: 40 }}>
        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
        <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} unit="%" />
        <YAxis type="category" dataKey="name" tick={{ fontSize: 11 }} width={110} />
        <Tooltip />
        <Legend />
        <Bar dataKey="reussite" name={t("chart.series.success")} stackId="a" fill="#10b981" isAnimationActive={false} />
        <Bar dataKey="echec" name={t("chart.series.fail")} stackId="a" fill="#ef4444" isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ProgressionChart({
  data,
}: {
  data: { period: string; average: number }[];
}) {
  const { t } = useI18n();
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="period" tick={{ fontSize: 11 }} />
        <YAxis domain={[0, 20]} tick={{ fontSize: 11 }} />
        <Tooltip />
        <Line type="monotone" dataKey="average" name={t("chart.series.mean")} stroke="#1d4ed8" strokeWidth={2} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function SegmentPie({
  data,
}: {
  data: { label: string; size: number }[];
}) {
  const { t } = useI18n();
  const rows = data.map((d) => ({ ...d, name: t(`segment.${d.label}`) }));
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={rows}
          dataKey="size"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label={(e) => `${e.name} (${e.size})`}
          isAnimationActive={false}
        >
          {rows.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function CorrelationHeatmap({ data }: { data: CorrelationMatrix }) {
  const { t } = useI18n();
  if (!data.matrix.length) {
    return <p className="text-sm text-slate-400">{t("common.noData")}</p>;
  }
  const color = (v: number) => {
    // Blue for positive, red for negative; opacity tracks the magnitude.
    const a = Math.min(1, Math.abs(v));
    return v >= 0 ? `rgba(29, 78, 216, ${a})` : `rgba(220, 38, 38, ${a})`;
  };
  const short = (l: string) => t(`corr.${l}`);
  return (
    <div className="overflow-x-auto">
      <table className="border-collapse text-xs">
        <thead>
          <tr>
            <th className="p-2"></th>
            {data.labels.map((l) => (
              <th key={l} className="p-2 font-medium text-slate-600">{short(l)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.matrix.map((row, i) => (
            <tr key={i}>
              <td className="p-2 font-medium text-slate-600">{short(data.labels[i])}</td>
              {row.map((v, j) => (
                <td
                  key={j}
                  className="p-3 text-center font-medium"
                  style={{ background: color(v), color: Math.abs(v) > 0.5 ? "white" : "#0f172a" }}
                >
                  {v.toFixed(2)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
