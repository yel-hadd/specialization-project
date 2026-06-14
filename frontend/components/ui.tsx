"use client";

// Small presentational components reused across pages.

import { useI18n } from "@/lib/i18n";
import { LOCALES, type Locale } from "@/lib/messages";

const SEGMENT_STYLES: Record<string, string> = {
  excellent: "bg-emerald-100 text-emerald-800",
  stable: "bg-sky-100 text-sky-800",
  moyen: "bg-amber-100 text-amber-800",
  fragile: "bg-orange-100 text-orange-800",
  a_risque: "bg-red-100 text-red-800",
};

const SEVERITY_STYLES: Record<string, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-amber-100 text-amber-800",
  low: "bg-slate-100 text-slate-700",
};

/** FR/EN toggle. Styled for dark backgrounds (sidebar, login). */
export function LanguageSwitcher({ className = "" }: { className?: string }) {
  const { locale, setLocale, t } = useI18n();
  return (
    <div className={className} aria-label={t("lang.label")}>
      <div className="flex rounded-lg border border-white/20 p-0.5 text-xs text-white">
        {LOCALES.map((l: Locale) => (
          <button
            key={l}
            onClick={() => setLocale(l)}
            aria-pressed={locale === l}
            className={`flex-1 rounded-md px-2 py-1 transition ${
              locale === l ? "bg-white/20 font-semibold" : "hover:bg-white/10"
            }`}
          >
            {l.toUpperCase()}
          </button>
        ))}
      </div>
    </div>
  );
}

/** Accessible "?" info bubble: shows instructional text on hover or focus. */
export function InfoTip({ text }: { text: string }) {
  return (
    <span className="group relative ml-1 inline-flex align-middle">
      <span
        tabIndex={0}
        role="img"
        aria-label={text}
        className="inline-flex h-4 w-4 cursor-help items-center justify-center rounded-full bg-slate-200 text-[10px] font-bold text-slate-600 hover:bg-slate-300"
      >
        ?
      </span>
      <span
        role="tooltip"
        className="pointer-events-none absolute bottom-full left-1/2 z-30 mb-1.5 w-56 -translate-x-1/2 rounded-md bg-slate-800 px-2.5 py-1.5 text-xs font-normal leading-snug text-white opacity-0 shadow-lg transition-opacity duration-150 group-hover:opacity-100 group-focus-within:opacity-100"
      >
        {text}
      </span>
    </span>
  );
}

export function SegmentBadge({ segment }: { segment: string }) {
  const { t } = useI18n();
  const cls = SEGMENT_STYLES[segment] || "bg-slate-100 text-slate-700";
  return <span className={`badge ${cls}`}>{t(`segment.${segment}`)}</span>;
}

export function SeverityBadge({ severity }: { severity: string }) {
  const { t } = useI18n();
  const cls = SEVERITY_STYLES[severity] || "bg-slate-100 text-slate-700";
  return <span className={`badge ${cls}`}>{t(`severity.${severity}`)}</span>;
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
  info,
}: {
  label: string;
  value: string | number;
  hint?: string;
  info?: string;
}) {
  return (
    <div className="card">
      <div className="flex items-center text-xs uppercase tracking-wide text-slate-500">
        <span>{label}</span>
        {info && <InfoTip text={info} />}
      </div>
      <div className="mt-1 text-3xl font-bold text-slate-900">{value}</div>
      {hint && <div className="mt-1 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}

/** Section heading used inside cards, with an optional info tooltip. */
export function CardTitle({ title, info }: { title: string; info?: string }) {
  return (
    <h2 className="mb-3 flex items-center font-semibold">
      <span>{title}</span>
      {info && <InfoTip text={info} />}
    </h2>
  );
}
