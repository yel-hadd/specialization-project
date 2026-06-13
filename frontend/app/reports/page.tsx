"use client";

import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { API_URL, getToken } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

export default function ReportsPage() {
  const { t } = useI18n();

  // Use fetch (not a plain link) to attach the JWT, then download the blob.
  async function open(format: "html" | "pdf") {
    const res = await fetch(`${API_URL}/reports/${format}`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!res.ok) {
      alert(t("reports.error"));
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    if (format === "pdf") {
      const a = document.createElement("a");
      a.href = url;
      a.download = "rapport_edutrack.pdf";
      a.click();
    } else {
      window.open(url, "_blank");
    }
    setTimeout(() => URL.revokeObjectURL(url), 10000);
  }

  return (
    <Shell>
      <PageTitle title={t("reports.title")} subtitle={t("reports.subtitle")} />
      <div className="card max-w-xl">
        <p className="mb-4 text-sm text-slate-600">{t("reports.desc")}</p>
        <div className="flex gap-3">
          <button className="btn" onClick={() => open("pdf")}>
            {t("reports.downloadPdf")}
          </button>
          <button className="btn-ghost" onClick={() => open("html")}>
            {t("reports.previewHtml")}
          </button>
        </div>
      </div>
    </Shell>
  );
}
