"use client";

import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { API_URL, getToken } from "@/lib/api";

export default function ReportsPage() {
  // Use fetch (not a plain link) to attach the JWT, then download the blob.
  async function open(format: "html" | "pdf") {
    const res = await fetch(`${API_URL}/reports/${format}`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!res.ok) {
      alert("Erreur lors de la generation du rapport");
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
      <PageTitle title="Generation de rapports" subtitle="Rapport pedagogique en PDF ou HTML" />
      <div className="card max-w-xl">
        <p className="text-sm text-slate-600 mb-4">
          Le rapport est genere a partir des donnees importees. Il reprend les indicateurs cles,
          la distribution des notes, l&apos;analyse par classe et par module, la segmentation et les
          etudiants a risque avec leurs recommandations.
        </p>
        <div className="flex gap-3">
          <button className="btn" onClick={() => open("pdf")}>
            Telecharger le PDF
          </button>
          <button className="btn-ghost" onClick={() => open("html")}>
            Apercu HTML
          </button>
        </div>
      </div>
    </Shell>
  );
}
