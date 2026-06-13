// Small presentational components reused across pages.

const SEGMENT_STYLES: Record<string, string> = {
  excellent: "bg-emerald-100 text-emerald-800",
  stable: "bg-sky-100 text-sky-800",
  regulier: "bg-sky-100 text-sky-800",
  moyen: "bg-amber-100 text-amber-800",
  en_progression: "bg-indigo-100 text-indigo-800",
  irregulier: "bg-orange-100 text-orange-800",
  fragile: "bg-orange-100 text-orange-800",
  a_risque: "bg-red-100 text-red-800",
};

const SEVERITY_STYLES: Record<string, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-amber-100 text-amber-800",
  low: "bg-slate-100 text-slate-700",
};

export function SegmentBadge({ segment }: { segment: string }) {
  const cls = SEGMENT_STYLES[segment] || "bg-slate-100 text-slate-700";
  return <span className={`badge ${cls}`}>{segment.replace("_", " ")}</span>;
}

export function SeverityBadge({ severity }: { severity: string }) {
  const cls = SEVERITY_STYLES[severity] || "bg-slate-100 text-slate-700";
  return <span className={`badge ${cls}`}>{severity}</span>;
}

export function PageTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
      {subtitle && <p className="text-sm text-slate-500">{subtitle}</p>}
    </div>
  );
}

export function KpiCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
  return (
    <div className="card">
      <div className="text-xs uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-1 text-3xl font-bold text-slate-900">{value}</div>
      {hint && <div className="mt-1 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}
