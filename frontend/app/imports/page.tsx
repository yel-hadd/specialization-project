"use client";

import { useState } from "react";
import Shell from "@/components/Shell";
import { PageTitle } from "@/components/ui";
import { uploadImport } from "@/lib/api";
import { useFetch } from "@/lib/useApi";
import type { ImportLog } from "@/lib/types";

interface ImportResult {
  status: string;
  rows_processed: number;
  rows_rejected: number;
  type: string;
  errors: string[];
  warnings: string[];
}

const STATUS_STYLES: Record<string, string> = {
  success: "bg-emerald-100 text-emerald-800",
  partial: "bg-amber-100 text-amber-800",
  failed: "bg-red-100 text-red-800",
};

export default function ImportsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [type, setType] = useState("auto");
  const [result, setResult] = useState<ImportResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const history = useFetch<ImportLog[]>(`/imports?_=${refresh}`);

  async function onUpload() {
    if (!file) return;
    setBusy(true);
    setResult(null);
    try {
      const res = (await uploadImport(file, type)) as ImportResult;
      setResult(res);
      setRefresh((r) => r + 1);
    } catch (e) {
      setResult({
        status: "failed",
        rows_processed: 0,
        rows_rejected: 0,
        type,
        errors: [String(e)],
        warnings: [],
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <Shell>
      <PageTitle title="Import de donnees" subtitle="Fichiers CSV ou Excel (etudiants, notes, absences)" />

      <div className="card mb-6">
        <div className="flex flex-wrap items-end gap-4">
          <div>
            <label className="text-sm font-medium text-slate-700">Fichier</label>
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block mt-1 text-sm"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700">Type</label>
            <select className="input mt-1 w-44" value={type} onChange={(e) => setType(e.target.value)}>
              <option value="auto">Detection automatique</option>
              <option value="students">Etudiants</option>
              <option value="grades">Notes</option>
              <option value="absences">Absences</option>
            </select>
          </div>
          <button className="btn" onClick={onUpload} disabled={!file || busy}>
            {busy ? "Import..." : "Importer"}
          </button>
        </div>

        {result && (
          <div className="mt-4 rounded-lg border border-slate-200 p-4">
            <div className="flex items-center gap-2">
              <span className={`badge ${STATUS_STYLES[result.status]}`}>{result.status}</span>
              <span className="text-sm text-slate-600">
                {result.rows_processed} lignes traitees, {result.rows_rejected} rejetees ({result.type})
              </span>
            </div>
            {result.warnings.length > 0 && (
              <ul className="mt-2 list-disc pl-5 text-xs text-amber-700">
                {result.warnings.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            )}
            {result.errors.length > 0 && (
              <ul className="mt-2 list-disc pl-5 text-xs text-red-700">
                {result.errors.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            )}
          </div>
        )}
      </div>

      <div className="card">
        <h2 className="font-semibold mb-3">Historique des imports</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="py-2">Date</th>
              <th>Fichier</th>
              <th>Type</th>
              <th>Traitees</th>
              <th>Rejetees</th>
              <th>Statut</th>
            </tr>
          </thead>
          <tbody>
            {history.data?.map((h) => (
              <tr key={h.id} className="border-b last:border-0">
                <td className="py-2">{new Date(h.imported_at).toLocaleString("fr-FR")}</td>
                <td className="font-mono text-xs">{h.filename}</td>
                <td>{h.type}</td>
                <td>{h.rows_processed}</td>
                <td>{h.rows_rejected}</td>
                <td><span className={`badge ${STATUS_STYLES[h.status]}`}>{h.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
